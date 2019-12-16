from pathlib import Path
from contextlib import contextmanager

# noinspection PyPackageRequirements
from docx import Document
# noinspection PyPackageRequirements
from docx.shared import Cm

from deplane.md_to_docx import insert_markdown, format_table


def _(x):
    """mark translations; actual translation later when we know language"""
    return x


OBLIGATION = {  # convert required to Obligation
    'mandatory': _('Mandatory'),
    'conditional': _('Mandatory, conditional'),
    'optional': _('Optional'),
}

FORMAT_TYPE = {  # convert datastore_type to Format Type
    'bigint': _('Integer'),
    'int': _('Integer'),
    'year': _('Integer'),
    'month': _('Integer'),
    'numeric': _('Numeric'),
    'money': _('Numeric'),
    'text': _('Text'),
    '_text': _('Text Array'),
    'date': _('Date'),
    'timestamp': _('Timestamp'),
}


def write_docx(schema, filename, trans, lang):
    """
    :param schema: recombinant-schema json dict
    :param filename: output docx filename to create
    :param trans: gettext translation object for language selected
    :param lang: language code selected (en/fr)
    """
    _ = trans.gettext

    document = Document(Path(__file__).parent / 'ENG_2_Colour.docx')
    section = document.sections[0]

    title = schema['title'][lang]

    section.different_first_page_header_footer = True
    section.first_page_header.paragraphs[0].text = ''
    section.header.paragraphs[0].text = _('Data Element Profile') + ' : ' + title

    # replace existing "TITLE" / "Subtitle" text
    document.paragraphs[0].runs[0].font.size = Cm(1.2)  # template title too large
    document.paragraphs[0].runs[0].text = _('Data Element Profile')
    document.paragraphs[0].runs[2].text = title
    # clear out the rest of the example text
    for para in reversed(document.paragraphs[2:]):
        delete_paragraph(para)

    document.add_heading(_('Overview'), 1)
    document.sections[-1].right_margin = Cm(2.54)  # restore right margin
    insert_markdown(document, _(
        'The purpose of this document is to provide supplemental information that is '
        'not provided in the *Centralized Contract Publishing System: Training Guide*. '
        'It will provide information to users on data elements within the Quarterly '
        'Contracts template.'
    ))

    if schema.get('front_matter'):
        insert_markdown(document, schema['front_matter'][lang])

    document.add_heading(_('Legend'), 1)
    document.add_paragraph(_(
        'The following sample table provides a description of each field you will see '
        'for all contract elements:'
    ))

    with build_table(
            document,
            [Cm(4.69), Cm(11.80)],
            top_color='d9d9d9',
            left_color='c6d9f1') as (trow, mrow):

        trow(_('Attribute'), _('Attribute Description'))
        trow(
            _('Field Name EN'),
            _('This text should correspond directly with the field name in your template in English'),
        )
        trow(
            _('Field Name FR'),
            _('This text should correspond directly with the field name in your template in French'),
        )
        trow(
            _('Description EN'),
            _('This provides a brief description of the element in English'),
        )
        trow(
            _('Description FR'),
            _('This provides a brief description of the element in French'),
        )
        mrow(
            _('Obligation'),
            _('''
Indicates whether the element is required to always or sometimes be present 
(i.e., contain a value). Options are:

- Mandatory
- Mandatory, conditional
- Optional'''),
        )
        mrow(
            _('Format Type'),
            _('''
Options are:

- Integer (e.g. page count, year or month number)
- Numeric (e.g. decimal, currency values)
- Text
- Text Array (e.g. one or more codes from a controlled list)
- Date (YYYY-MM-DD)
- Timestamp (YYYY-MM-DD hh:mm:ss)''')
        )
        trow(
            _('Validation'),
            _('''
Describes the condition or conditions according to which a value shall be present.
Indicates what the system will accept in this field.'''),
        )
        trow(
            _('Example Value'),
            _(
                'Provide one or more real examples of the values that may appear, '
                'e.g. “CODE1” or “Family Services Reform Program”'
            ),
        )

    document.add_paragraph(_('\nControlled List Values:'))
    with build_table(
            document,
            [Cm(3.69), Cm(6.4), Cm(6.4)],
            top_color='d9d9d9') as (trow, mrow):
        trow(_('Code'), _('English'), _('French'))
        trow('CODE1', _('English Description 1'), _('French Description 1'))
        trow('CODE2', _('English Description 2'), _('French Description 2'))

    document.add_page_break()

    for rnum, res in enumerate(schema['resources'], 1):
        document.add_heading(res['title'][lang] + '\n', 1)

        for fnum, field in enumerate(res['fields'], 1):
            document.add_heading(f'{rnum}-{fnum} {field["label"][lang]}\n', 2)
            with build_table(
                    document,
                    [Cm(4.69), Cm(11.80)],
                    top_color='d9d9d9',
                    left_color='c6d9f1') as (trow, mrow):
                trow(_('Attribute'), _('Attribute Description'))
                trow(_('Field Name EN'), field['label']['en'])
                trow(_('Field Name FR'), field['label']['fr'])
                trow(_('ID'), field['id'])
                mrow(_('Description EN'), field.get('description', {}).get('en', ''))
                mrow(_('Description FR'), field.get('description', {}).get('fr', ''))
                trow(_('Obligation'), _(OBLIGATION[field.get('obligation')]))
                mrow(_('Format Type'), _(FORMAT_TYPE[field['datastore_type']]))
                mrow(_('Validation'), field.get('validation', {}).get(lang, ''))
                eg = res['example_record'].get(field['id'], '')
                if isinstance(eg, list):
                    eg = ','.join(eg)
                trow(_('Example Value'), str(eg))

            if 'choices' in field:
                document.add_paragraph(_('\nControlled List Values:'))
                with build_table(
                        document,
                        [Cm(3.69), Cm(6.4), Cm(6.4)],
                        top_color='d9d9d9') as (trow, mrow):
                    trow(_('Code'), _('English'), _('French'))
                    for c, v in field['choices'].items():
                        if isinstance(v, dict):
                            trow(c, v.get('en', ''), v.get('fr', ''))
                        else:
                            trow(c, v, v)

            document.add_paragraph('\n\n')

        document.add_page_break()

    document.save(filename)


def delete_paragraph(para):
    p = para._element
    p.getparent().remove(p)
    p._p = p._element = None


@contextmanager
def build_table(document, widths, **format_args):
    """
    Context manager for building a table with text rows and markdown rows

    Yields (trow, mrow) functions for adding text/markdown rows to the table
    """
    table = document.add_table(rows=0, cols=len(widths))
    table.autofit = False
    def trow(first, *rest):
        """Add a text row to table"""
        cells = table.add_row().cells
        cells[0].text = first
        for i, c in enumerate(rest, 1):
            cells[i].text = c

    def mrow(first, *rest):
        """Add a markdown row to table"""
        cells = table.add_row().cells
        cells[0].text = first
        for i, c in enumerate(rest, 1):
            if c:
                delete_paragraph(cells[i].paragraphs[0])
            insert_markdown(cells[i], c)

    yield trow, mrow

    format_table(table, widths=widths, **format_args)