"""Test click."""
import click


@click.command()
def main() -> None:
    """Run.

    :rtype: None
    """
    click.echo("Hello World!")
