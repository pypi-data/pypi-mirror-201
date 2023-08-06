"""Console script for shag."""

import click


@click.command()
def main():
    """Main entrypoint."""
    click.echo("shag")
    click.echo("=" * len("shag"))
    click.echo("Implementation of spatial hashing approximate Gaussian processes")


if __name__ == "__main__":
    main()  # pragma: no cover
