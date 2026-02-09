import os
from ruamel.yaml import YAML
import click
from docx import Document

from replane.engineer import read_docx


@click.command()
@click.argument('yaml_file', type=click.Path())
@click.argument('docx_file', type=click.Path())
@click.option('-l', '--max-line', default=130,
              help='Max line length to write to YAML')
def cli(yaml_file, docx_file, max_line=130):
    """
    Create YAML based on Data Element Profile docx
    """
    cli_impl(yaml_file, docx_file, max_line=max_line)


def cli_impl(yaml_file, docx_file, max_line=130):
    _yaml = YAML()
    _yaml.preserve_quotes = True
    _yaml.width = max_line
    # TODO: this assumes that we already have a geno with resources in it.
    #       we need to be able to create a blank YAML
    with open(yaml_file) as f:
        geno = _yaml.load(f)
    document = Document(docx_file)
    dep_dict = read_docx(document)
    for resource in geno['resources']:
        for field in resource['fields']:
            if field['datastore_id'] in dep_dict:
                comments = dep_dict[field['datastore_id']].pop('YAML_COMMENTS', None)
                example = dep_dict[field['datastore_id']].pop('example', None)
                # TODO: check to make sure no choice values were removed/modified.
                #       raise an Exception if they were, as that would mean a data migration.
                if 'choices_file' in field and 'choices' in dep_dict[field['datastore_id']]:
                    choices_dict = dep_dict[field['datastore_id']].pop('choices')
                    choices_file = os.path.dirname(yaml_file) + '/' + field['choices_file']
                    with open(choices_file, 'w') as f:
                        _yaml.dump(choices_dict, f)
                for _directive in dep_dict[field['datastore_id']]:
                    if _directive in field and field[_directive] != dep_dict[field['datastore_id']][_directive]:
                        field[_directive] = dep_dict[field['datastore_id']][_directive]
                if comments:
                    field.yaml_set_start_comment(comment=comments, indent=2)
                if example and example != resource['examples']['record'][field['datastore_id']]:
                    resource['examples']['record'][field['datastore_id']] = example
                if 'form_attrs' in field and 'maxlength' in field['form_attrs'] and 'max_chars' in dep_dict[field['datastore_id']]:
                    field['form_attrs']['maxlength'] = dep_dict[field['datastore_id']]['max_chars']
    with open(yaml_file, 'w') as f:
        _yaml.dump(geno, f)
        