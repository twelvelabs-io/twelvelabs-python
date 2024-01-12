import click


class Environment:
    pass


pass_environment = click.make_pass_decorator(Environment, ensure=True)
