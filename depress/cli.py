import click
import requests

from depress.publish import write_docx

@click.command()
@click.argument('lang')
@click.argument('url')
@click.argument('filename')
def cli(lang, url, filename):
    geno = requests.get(url)
    write_docx(filename)
