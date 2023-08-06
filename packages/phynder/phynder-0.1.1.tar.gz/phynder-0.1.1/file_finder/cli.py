import click
from file_finder.finder import finder
from file_finder.exceptions import FileFinderError

def cli():
    try:
        finder()
    except FileFinderError as err:
        click.echo(click.style(f"❌ {err}", bg='black', fg='red', italic=True))