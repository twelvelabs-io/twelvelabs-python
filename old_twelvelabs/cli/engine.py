import click

from .environment import pass_environment


@click.group()
def cli():
    pass


@cli.command()
@pass_environment
def list(env):
    print(env.client)
    click.echo("engine list")
