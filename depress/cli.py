from pathlib import Path
import gettext

import click
import requests

from depress.publish import write_docx

@click.command()
@click.argument('lang')
@click.argument('url')
@click.argument('filename')
def cli(lang, url, filename):
    trans = gettext.translation(
        'depress',
        Path(__file__).parent / 'i18n',
        languages=[lang],
    )
    trans.install()
    geno = requests.get(url)
    write_docx(filename, trans)
