import typing


def _literal_values(alias):
    literal_type = next(argument for argument in typing.get_args(alias) if typing.get_origin(argument) is typing.Literal)
    return typing.get_args(literal_type)


def test_legacy_responses_type_aliases_keep_all_public_import_paths():
    from twelvelabs import ResponseAnnotationType, ResponseOutputItemRole, ResponseOutputItemType
    from twelvelabs.core.pydantic_utilities import parse_obj_as
    from twelvelabs.types import (
        ResponseAnnotationType as TypeResponseAnnotationType,
    )
    from twelvelabs.types import (
        ResponseOutputItemRole as TypeResponseOutputItemRole,
    )
    from twelvelabs.types import (
        ResponseOutputItemType as TypeResponseOutputItemType,
    )
    from twelvelabs.types.response_annotation_type import ResponseAnnotationType as ModuleResponseAnnotationType
    from twelvelabs.types.response_output_item_role import ResponseOutputItemRole as ModuleResponseOutputItemRole
    from twelvelabs.types.response_output_item_type import ResponseOutputItemType as ModuleResponseOutputItemType

    assert ResponseOutputItemType is TypeResponseOutputItemType is ModuleResponseOutputItemType
    assert ResponseOutputItemRole is TypeResponseOutputItemRole is ModuleResponseOutputItemRole
    assert ResponseAnnotationType is TypeResponseAnnotationType is ModuleResponseAnnotationType
    assert _literal_values(ResponseOutputItemType) == ("message", "function_call", "function_call_output")
    assert _literal_values(ResponseOutputItemRole) == ("assistant",)
    assert _literal_values(ResponseAnnotationType) == ("video_citation", "image_citation", "collection_citation")
    for value in _literal_values(ResponseOutputItemType):
        assert parse_obj_as(ResponseOutputItemType, value) == value
    for value in _literal_values(ResponseOutputItemRole):
        assert parse_obj_as(ResponseOutputItemRole, value) == value
    for value in _literal_values(ResponseAnnotationType):
        assert parse_obj_as(ResponseAnnotationType, value) == value
