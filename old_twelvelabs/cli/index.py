import click


@click.group()
def cli():
    pass


@cli.command()
def list():
    click.echo("index list")
