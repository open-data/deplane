from pathlib import Path
import gettext

import yaml
import click
import requests
from requests.exceptions import InvalidSchema, MissingSchema

from deplane.publish import write_docx


@click.command()
@click.argument('lang', type=click.Choice(['en', 'fr']))
@click.argument('url')
@click.argument('filename', type=click.Path())
def cli(lang, url, filename):
    """
    Create Data Element Profile docx based on ckanext-recombinant json schema
    """
    if lang == 'en':
        trans = gettext.NullTranslations()
    else:
        trans = gettext.translation(
            'deplane',
            Path(__file__).parent / 'i18n',
            languages=[lang],
        )
        trans.install()
    try:
        geno = requests.get(url).json()
    except (InvalidSchema, MissingSchema):
        with open(url) as f:
            geno = yaml.safe_load(f)
    write_docx(geno, filename, trans, lang)
