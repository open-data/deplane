from pathlib import Path

# noinspection PyPackageRequirements
from docx import Document
from docx.shared import Cm

from deplane.md_to_docx import insert_markdown, format_table


def write_docx(schema, filename, trans, lang):
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

    table = document.add_table(rows=0, cols=2)
    table.autofit = False

    def trow(att, desc):
        """Add a text row to table"""
        cells = table.add_row().cells
        cells[0].text = att
        cells[1].text = desc

    def mrow(att, md):
        """Add a markdown row to table"""
        cells = table.add_row().cells
        cells[0].text = att
        delete_paragraph(cells[1].paragraphs[0])
        insert_markdown(cells[1], md)
        return cells[1]

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
    trow(
        _('Condition'),
        _('Describes the condition or conditions according to which a value shall be present'),
    )
    mrow(
        _('Format Type'),
        _('''
Indicates the required format of the values, if any, at the file level.
“Free text” indicates that the value may be input using natural language
(i.e., there is no constraint) while “single choice” or “multiple choice”
indicates the values are restricted to a controlled list.)

Controlled List Values:

Code | English | French
--- | --- | ---
CODE1 | English Description 1 | French Description 1
CODE2 | English Description 2 | French Description 2'''),
    )
    trow(
        _('Validation'),
        _('Indicates what the system will accept in this field'),
    )
    trow(
        _('Validation Errors'),
        _(
            'This section indicates when an error has been made. '
            'It will detail the error and provide instruction on how to correct it.'
        ),
    )
    trow(
        _('Example Value'),
        _(
            'Provide one or more real examples of the values that may appear, '
            'e.g. “CODE1” or “Family Services Reform Program”'
        ),
    )

    format_table(
        table,
        widths=[Cm(4.69), Cm(11.80)],
        top_color='d9d9d9',
        left_color='c6d9f1',
    )

    document.add_page_break()

    for rnum, res in enumerate(schema['resources'], 1):
        document.add_heading(res['title'][lang] + '\n', 1)

        for fnum, field in enumerate(res['fields'], 1):
            document.add_heading(f'{rnum}-{fnum} {field["label"][lang]}\n', 2)
            table = document.add_table(rows=0, cols=2)
            table.autofit = False
            trow(_('Attribute'), _('Attribute Description'))
            trow(_('Field Name EN'), field['label']['en'])
            trow(_('Field Name FR'), field['label']['fr'])
            trow(_('ID'), field['id'])
            mrow(_('Description EN'), field.get('description', {}).get('en', ''))
            mrow(_('Description FR'), field.get('description', {}).get('fr', ''))
            trow(_('Obligation'), field.get('obligation', {}).get(lang, ''))
            trow(_('Condition'), '')  # FIXME not recorded?
            cell = mrow(_('Format Type'), field.get('format_type', {}).get(lang, ''))

            if 'choices' in field:
                pass
            trow(_('Validation'), '')  # FIXME not recorded
            trow(_('Validation Errors'), '')  # FIXME not recorded

            eg = res['example_record'].get(field['id'], '')
            if isinstance(eg, list):
                eg = ','.join(eg)
            trow(_('Example Value'), str(eg))

            format_table(
                table,
                widths=[Cm(4.69), Cm(11.80)],
                top_color='d9d9d9',
                left_color='c6d9f1',
            )
            document.add_paragraph('\n\n')
        document.add_page_break()

    document.save(filename)


def delete_paragraph(para):
    p = para._element
    p.getparent().remove(p)
    p._p = p._element = None