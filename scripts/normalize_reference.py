"""Normalize Fern's raw streaming examples to the public SDK iterator API.

Fern currently puts raw-client snippets into public client reference sections.
This source-aware pass changes only ``for ... in response.data`` when the
response was assigned from a public client method whose resolved return hint
is an iterator. At module level, it also changes ``yield value`` to
``print(value)`` inside those verified iterator loops so the reference example
is valid Python. It intentionally leaves raw responses and model ``.data``
fields alone.
"""

import argparse
import ast
import asyncio
import collections.abc
import inspect
import sys
import typing
from pathlib import Path
from typing import Any, Dict, Iterable, List, NamedTuple, Optional, Sequence, Set, Tuple, Union

SDK_ROOT = Path(__file__).resolve().parents[1]
REFERENCE_PATH = SDK_ROOT / "reference.md"


class CodeFence(NamedTuple):
    start: int
    end: int
    source: str
    opening_line: int


class NormalizationError(Exception):
    """Raised when a candidate generated example cannot be classified safely."""


class PublicClientResolver:
    """Resolve public SDK methods without making HTTP requests."""

    def __init__(self) -> None:
        import httpx

        from twelvelabs import AsyncTwelveLabs, TwelveLabs

        self.requests: List[Any] = []

        def reject_sync_request(request: Any) -> Any:
            self.requests.append(request)
            raise AssertionError("reference normalization must not make HTTP requests")

        async def reject_async_request(request: Any) -> Any:
            self.requests.append(request)
            raise AssertionError("reference normalization must not make HTTP requests")

        class RejectingSyncTransport(httpx.BaseTransport):
            def handle_request(self, request: Any) -> Any:
                return reject_sync_request(request)

        class RejectingAsyncTransport(httpx.AsyncBaseTransport):
            async def handle_async_request(self, request: Any) -> Any:
                return await reject_async_request(request)

        self._sync_httpx = httpx.Client(transport=RejectingSyncTransport())
        self._async_httpx = httpx.AsyncClient(transport=RejectingAsyncTransport())
        self._sync_client = TwelveLabs(
            api_key="REFERENCE_NORMALIZER_NO_NETWORK",
            base_url="https://reference-normalizer.invalid",
            httpx_client=self._sync_httpx,
        )
        self._async_client = AsyncTwelveLabs(
            api_key="REFERENCE_NORMALIZER_NO_NETWORK",
            base_url="https://reference-normalizer.invalid",
            httpx_client=self._async_httpx,
        )
        self._clients = {
            "TwelveLabs": self._sync_client,
            "AsyncTwelveLabs": self._async_client,
        }

    def close(self) -> None:
        self._sync_httpx.close()
        asyncio.run(self._async_httpx.aclose())

    def instance(self, client_kind: str) -> Any:
        return self._clients[client_kind]

    def returns_iterator(self, client_kind: str, attributes: Sequence[str], awaited: bool) -> bool:
        if "with_raw_response" in attributes:
            return False
        if not attributes:
            raise NormalizationError("public client call has no method path")

        value = self.instance(client_kind)
        for attribute in attributes:
            try:
                value = getattr(value, attribute)
            except AttributeError as exc:
                path = ".".join(attributes)
                raise NormalizationError(
                    "cannot resolve public SDK method {!r} on {}".format(path, client_kind)
                ) from exc

        if not callable(value):
            raise NormalizationError("resolved public SDK endpoint is not callable")
        if inspect.iscoroutinefunction(value) != awaited:
            raise NormalizationError(
                "public SDK method {!r} has an unexpected await shape".format(".".join(attributes))
            )
        try:
            return_hint = typing.get_type_hints(value).get("return")
        except (NameError, TypeError) as exc:
            raise NormalizationError(
                "cannot resolve return annotation for public SDK method {!r}".format(".".join(attributes))
            ) from exc
        if return_hint is None:
            raise NormalizationError(
                "public SDK method {!r} has no resolved return annotation".format(".".join(attributes))
            )

        iterator_origins = {
            typing.Iterator,
            typing.AsyncIterator,
            typing.Generator,
            typing.AsyncGenerator,
            collections.abc.Iterator,
            collections.abc.AsyncIterator,
            collections.abc.Generator,
            collections.abc.AsyncGenerator,
        }
        return typing.get_origin(return_hint) in iterator_origins


def _line_offsets(source: str) -> Tuple[List[str], List[int]]:
    lines = source.splitlines(keepends=True)
    if not lines:
        lines = [""]
    offsets = []
    total = 0
    for line in lines:
        offsets.append(total)
        total += len(line)
    return lines, offsets


def _source_offset(lines: Sequence[str], offsets: Sequence[int], line: int, column: int) -> int:
    if line < 1 or line > len(lines):
        raise NormalizationError("AST source location is outside its fenced code block")
    encoded_prefix = lines[line - 1].encode("utf-8")[:column]
    try:
        character_column = len(encoded_prefix.decode("utf-8"))
    except UnicodeDecodeError as exc:
        raise NormalizationError("AST column does not align to UTF-8 source") from exc
    return offsets[line - 1] + character_column


def _node_start(source: str, lines: Sequence[str], offsets: Sequence[int], node: ast.AST) -> int:
    return _source_offset(lines, offsets, node.lineno, node.col_offset)  # type: ignore[attr-defined]


def _node_end(source: str, lines: Sequence[str], offsets: Sequence[int], node: ast.AST) -> int:
    return _source_offset(lines, offsets, node.end_lineno, node.end_col_offset)  # type: ignore[attr-defined]


def _fenced_python_blocks(markdown: str) -> List[CodeFence]:
    lines, offsets = _line_offsets(markdown)
    blocks: List[CodeFence] = []
    fence_character: Optional[str] = None
    fence_length = 0
    fence_is_python = False
    body_start = 0
    opening_line = 0

    for index, line in enumerate(lines):
        stripped = line.lstrip(" ")
        indentation = len(line) - len(stripped)
        content = stripped.rstrip("\r\n")

        if fence_character is None:
            if indentation > 3 or not content:
                continue
            character = content[0]
            if character not in ("`", "~"):
                continue
            run_length = len(content) - len(content.lstrip(character))
            if run_length < 3:
                continue
            info = content[run_length:].strip()
            if character == "`" and "`" in info:
                continue
            fence_character = character
            fence_length = run_length
            fence_is_python = info.split(None, 1)[0].lower() in ("python", "python3") if info else False
            body_start = offsets[index] + len(line)
            opening_line = index + 1
            continue

        if indentation > 3 or not content or content[0] != fence_character:
            continue
        run_length = len(content) - len(content.lstrip(fence_character))
        if run_length < fence_length or content[run_length:].strip():
            continue
        closing_start = offsets[index]
        if fence_is_python:
            blocks.append(CodeFence(body_start, closing_start, markdown[body_start:closing_start], opening_line))
        fence_character = None
        fence_length = 0
        fence_is_python = False

    if fence_character is not None:
        raise NormalizationError("unterminated Markdown code fence opened on line {}".format(opening_line))
    return blocks


def _client_constructor_imports(tree: ast.Module) -> Dict[str, str]:
    constructors: Dict[str, str] = {}
    for node in tree.body:
        if not isinstance(node, ast.ImportFrom) or node.module != "twelvelabs":
            continue
        for imported in node.names:
            if imported.name in ("TwelveLabs", "AsyncTwelveLabs"):
                constructors[imported.asname or imported.name] = imported.name
    return constructors


def _attribute_chain(node: ast.AST) -> Optional[List[str]]:
    attributes: List[str] = []
    current = node
    while isinstance(current, ast.Attribute):
        attributes.append(current.attr)
        current = current.value
    if not isinstance(current, ast.Name):
        return None
    attributes.reverse()
    return [current.id] + attributes


def _assigned_names(target: ast.AST) -> Iterable[str]:
    if isinstance(target, ast.Name):
        yield target.id
    elif isinstance(target, (ast.Tuple, ast.List)):
        for element in target.elts:
            for name in _assigned_names(element):
                yield name


_AMBIGUOUS = object()


class _ExampleAnalyzer(ast.NodeVisitor):
    def __init__(self, source: str, resolver: PublicClientResolver, tree: ast.Module) -> None:
        self.source = source
        self.resolver = resolver
        self.lines, self.offsets = _line_offsets(source)
        self.constructors = _client_constructor_imports(tree)
        self.clients: Dict[Tuple[Tuple[str, ...], str], Any] = {}
        self.responses: Dict[Tuple[Tuple[str, ...], str], Any] = {}
        self.edits_found: List[Tuple[int, int, str]] = []
        self.scope: List[str] = []
        self.control_flow_depth = 0

    def _record_assignment(self, target: ast.AST, value: Optional[ast.AST]) -> None:
        constructor_name = None
        if isinstance(value, ast.Call) and isinstance(value.func, ast.Name):
            constructor_name = self.constructors.get(value.func.id)
        for name in _assigned_names(target):
            key = (tuple(self.scope), name)
            self.clients[key] = constructor_name
            self.responses[key] = value

    def visit_Assign(self, node: ast.Assign) -> None:
        for target in node.targets:
            self._record_assignment(target, node.value)
        self.generic_visit(node)

    def visit_AnnAssign(self, node: ast.AnnAssign) -> None:
        self._record_assignment(node.target, node.value)
        self.generic_visit(node)

    def _visit_scope(self, node: ast.AST, label: str) -> None:
        old_clients = self.clients
        old_responses = self.responses
        self.clients = dict(old_clients)
        self.responses = dict(old_responses)
        self.scope.append(label)
        self.generic_visit(node)
        self.scope.pop()
        self.clients = old_clients
        self.responses = old_responses

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self._visit_scope(node, "function:{}:{}".format(node.name, node.lineno))

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self._visit_scope(node, "async-function:{}:{}".format(node.name, node.lineno))

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        self._visit_scope(node, "class:{}:{}".format(node.name, node.lineno))

    def visit_For(self, node: ast.For) -> None:
        self._record_iteration(node.iter, node)
        self._visit_ambiguous_compound(node)

    def visit_AsyncFor(self, node: ast.AsyncFor) -> None:
        self._record_iteration(node.iter, node)
        self._visit_ambiguous_compound(node)

    def visit_If(self, node: ast.If) -> None:
        self._visit_ambiguous_compound(node)

    def visit_While(self, node: ast.While) -> None:
        self._visit_ambiguous_compound(node)

    def visit_With(self, node: ast.With) -> None:
        self._visit_ambiguous_compound(node)

    def visit_AsyncWith(self, node: ast.AsyncWith) -> None:
        self._visit_ambiguous_compound(node)

    def visit_Try(self, node: ast.Try) -> None:
        self._visit_ambiguous_compound(node)

    def visit_NamedExpr(self, node: ast.NamedExpr) -> None:
        for name in _assigned_names(node.target):
            key = (tuple(self.scope), name)
            self.clients[key] = _AMBIGUOUS
            self.responses[key] = _AMBIGUOUS
        self.generic_visit(node)

    def _visit_ambiguous_compound(self, node: ast.AST) -> None:
        names = self._stored_names(node)
        prior_clients = dict(self.clients)
        prior_responses = dict(self.responses)
        self.control_flow_depth += 1
        self.generic_visit(node)
        self.control_flow_depth -= 1
        self.clients = prior_clients
        self.responses = prior_responses
        scope = tuple(self.scope)
        for name in names:
            key = (scope, name)
            self.clients[key] = _AMBIGUOUS
            self.responses[key] = _AMBIGUOUS

    def _stored_names(self, node: ast.AST) -> Set[str]:
        names: Set[str] = set()

        class StoreVisitor(ast.NodeVisitor):
            def visit_FunctionDef(self, child: ast.FunctionDef) -> None:
                return

            def visit_AsyncFunctionDef(self, child: ast.AsyncFunctionDef) -> None:
                return

            def visit_ClassDef(self, child: ast.ClassDef) -> None:
                return

            def visit_Name(self, child: ast.Name) -> None:
                if isinstance(child.ctx, ast.Store):
                    names.add(child.id)

        StoreVisitor().visit(node)
        return names

    def _record_iteration(self, iterable: ast.AST, loop: Union[ast.For, ast.AsyncFor]) -> None:
        data_attribute = iterable if isinstance(iterable, ast.Attribute) and iterable.attr == "data" else None
        response: ast.AST
        if data_attribute is not None:
            response = data_attribute.value
        else:
            response = iterable
        if not isinstance(response, ast.Name):
            return
        line = loop.lineno
        key = (tuple(self.scope), response.id)
        response_value = self.responses.get(key)
        if response_value is _AMBIGUOUS:
            raise NormalizationError(
                "ambiguous assignment flow for response.data on line {}".format(line)
            )
        if response_value is None:
            return

        awaited = isinstance(response_value, ast.Await)
        call = response_value.value if awaited else response_value
        if not isinstance(call, ast.Call):
            return
        chain = _attribute_chain(call.func)
        if chain is None or not chain:
            return
        client_key = (tuple(self.scope), chain[0])
        client_kind = self.clients.get(client_key)
        if client_kind is _AMBIGUOUS:
            raise NormalizationError(
                "ambiguous public-client binding for response.data on line {}".format(line)
            )
        if client_kind is None:
            return
        if len(chain) < 2:
            raise NormalizationError("public SDK call has no endpoint path")
        attributes = chain[1:]
        if "with_raw_response" in attributes:
            return
        if not self.resolver.returns_iterator(client_kind, attributes, awaited):
            return
        if self.control_flow_depth:
            raise NormalizationError(
                "public iterator example on line {} is inside ambiguous control flow".format(line)
            )

        if data_attribute is not None:
            value_end = _node_end(self.source, self.lines, self.offsets, data_attribute.value)
            attribute_end = _node_end(self.source, self.lines, self.offsets, data_attribute)
            if self.source[value_end:attribute_end] != ".data":
                raise NormalizationError(
                    "unsupported formatting for response.data on line {}".format(line)
                )
            self.edits_found.append((value_end, attribute_end, ""))

    def edits(self) -> List[Tuple[int, int, str]]:
        tree = ast.parse(self.source)
        self.visit(tree)
        self.edits_found.extend(
            _module_level_yield_edits(self.source, self.lines, self.offsets, tree)
        )
        return self.edits_found


def _module_level_yield_edits(
    source: str, lines: Sequence[str], offsets: Sequence[int], tree: ast.Module
) -> List[Tuple[int, int, str]]:
    edits: List[Tuple[int, int, str]] = []
    supported_yields: Set[ast.Yield] = set()

    class ModuleYieldVisitor(ast.NodeVisitor):
        def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
            return

        def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
            return

        def visit_ClassDef(self, node: ast.ClassDef) -> None:
            return

        def visit_Expr(self, node: ast.Expr) -> None:
            if isinstance(node.value, ast.Yield):
                supported_yields.add(node.value)
            self.generic_visit(node)

        def visit_Yield(self, node: ast.Yield) -> None:
            if node not in supported_yields or node.value is None:
                raise NormalizationError(
                    "unsupported module-level yield form on line {}".format(node.lineno)
                )
            value_start = _node_start(source, lines, offsets, node.value)
            value_end = _node_end(source, lines, offsets, node.value)
            yield_start = _node_start(source, lines, offsets, node)
            yield_end = _node_end(source, lines, offsets, node)
            edits.append((yield_start, yield_end, "print({})".format(source[value_start:value_end])))
            self.generic_visit(node)

        def visit_YieldFrom(self, node: ast.YieldFrom) -> None:
            raise NormalizationError(
                "unsupported module-level yield-from form on line {}".format(node.lineno)
            )

    ModuleYieldVisitor().visit(tree)
    return edits


def normalize_python_source(source: str, resolver: PublicClientResolver) -> Tuple[str, int]:
    try:
        tree = ast.parse(source)
    except SyntaxError as exc:
        raise NormalizationError(
            "invalid Python example at line {}: {}".format(exc.lineno, exc.msg)
        ) from exc
    analyzer = _ExampleAnalyzer(source, resolver, tree)
    edits = analyzer.edits()
    for start, end, replacement in sorted(edits, reverse=True):
        source = source[:start] + replacement + source[end:]
    return source, 1 if edits else 0


def normalize_reference(markdown: str, resolver: PublicClientResolver) -> Tuple[str, int]:
    blocks = _fenced_python_blocks(markdown)
    normalized = markdown
    changed = 0
    for block in reversed(blocks):
        new_source, count = normalize_python_source(block.source, resolver)
        if count:
            changed += 1
        if count:
            normalized = normalized[:block.start] + new_source + normalized[block.end:]
    return normalized, changed


def _main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true", help="fail if reference.md needs normalization")
    mode.add_argument("--write", action="store_true", help="normalize reference.md in place")
    args = parser.parse_args()

    sys.path.insert(0, str(SDK_ROOT / "src"))
    original = REFERENCE_PATH.read_text(encoding="utf-8")
    resolver = PublicClientResolver()
    try:
        normalized, count = normalize_reference(original, resolver)
        if resolver.requests:
            raise NormalizationError("unexpected HTTP request during reference normalization")
    finally:
        resolver.close()

    if args.write:
        if count:
            with REFERENCE_PATH.open("w", encoding="utf-8", newline="") as reference_file:
                reference_file.write(normalized)
        print("Normalized {} Python reference example block(s) in {}".format(count, REFERENCE_PATH))
        return 0

    if count:
        print(
            "reference.md has {} unnormalized Python example block(s); run `poetry run python scripts/normalize_reference.py --write` after Fern generation".format(
                count
            ),
            file=sys.stderr,
        )
        return 1
    print("reference.md public streaming examples are normalized")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(_main())
    except NormalizationError as exc:
        print("reference normalization failed: {}".format(exc), file=sys.stderr)
        raise SystemExit(2)
