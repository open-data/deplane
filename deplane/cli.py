from pathlib import Path
import gettext

from typing import Optional

import yaml
import click
import requests
from requests.exceptions import InvalidSchema, MissingSchema

from deplane.publish import write_docx


@click.command()
@click.argument('lang', type=click.Choice(['en', 'fr']))
@click.argument('url')
@click.argument('filename', type=click.Path())
@click.option('-g', '--github', type=click.STRING,
              help='Github branch of open-data/ckanext-canada to use' \
                   ' as the remote YAML Schema for more advanced DEPs.')
def cli(lang, url, filename, github: Optional[str] = None):
    """
    Create Data Element Profile docx based on ckanext-recombinant json schema
    """
    cli_impl(lang, url, filename, github)


def cli_impl(lang, url, filename, github):
    print('Using translation file for language: %s' % lang)
    french_trans = gettext.translation(
        'deplane',
        Path(__file__).parent / 'i18n',
        languages=['fr'],
    )
    french_trans.install()
    if lang == 'en':
        trans = gettext.NullTranslations()
    else:
        trans = french_trans
    if github:
        t = url.rpartition('/')[-1].replace('.json', '')
        r = f'https://raw.githubusercontent.com/open-data/ckanext-canada/refs/heads/{github}/ckanext/canada/tables/{t}.yaml'
        print('Fetching geno for %s from Github remote: %s' % (t, r))
        f = requests.get(r).content
        geno = yaml.safe_load(f)
        write_docx(geno, filename, trans, lang, french_trans, remote_choices=f'https://raw.githubusercontent.com/open-data/ckanext-canada/refs/heads/{github}/ckanext/canada/tables')
        return
    try:
        geno = requests.get(url).json()
        print('Fetching geno from remote JSON: %s' % url)
    except (InvalidSchema, MissingSchema):
        with open(url) as f:
            geno = yaml.safe_load(f)
        print('Fetching geno from file: %s' % url)
    write_docx(geno, filename, trans, lang, french_trans)
