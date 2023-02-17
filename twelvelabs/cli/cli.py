import click

from .. import APIClient
from . import engine, index, task
from .environment import pass_environment

API_KEY = "a"


@click.group()
@pass_environment
def cli(env):
    env.client = APIClient(api_key=API_KEY)


cli.add_command(engine.cli, "engine")
cli.add_command(index.cli, "index")
cli.add_command(task.cli, "task")
