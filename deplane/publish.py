# noinspection PyPackageRequirements
from docx import Document


def write_docx(schema, filename, trans, lang):
    _ = trans.gettext

    document = Document()
    section = document.sections[0]

    title = schema['title'][lang]

    section.different_first_page_header_footer = True
    section.first_page_header.paragraphs[0].text = _(
        'Centralized Publishing System for Proactive Disclosure'
    )
    section.header.paragraphs[0].text = _('Template Guide: {title}').format(title=title)
    document.add_heading(_('Data Element Profile: {title}').format(title=title), 0)
    document.add_paragraph(_('Open Government Team'))
    document.add_page_break()

    document.add_heading(_('Legend'), 1)
    document.add_paragraph(_(
        'The following sample table provides a description of each field you will see '
        'for all contract elements:'
    ))

    table = document.add_table(rows=0, cols=2)
    def trow(att, desc):
        cells = table.add_row().cells
        cells[0].text = att
        cells[1].text = desc

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
    cells = table.add_row().cells
    cells[0].text = _('Obligation')
    cells[1].text = _(
        'Indicates whether the element is required to always or sometimes be present '
        '(i.e., contain a value). Options are:'
    )
    cells[1].add_paragraph(_('Mandatory'), style='List Bullet')
    cells[1].add_paragraph(_('Mandatory, conditional'), style='List Bullet')
    cells[1].add_paragraph(_('Optional'), style='List Bullet')
    '''
Condition
Describes the condition or conditions according to which a value shall be present
Format Type
Indicates the required format of the values, if any, at the file level.  “Free text” indicates that the value may be input using natural language (i.e., there is no constraint) while “single choice” or “multiple choice” indicates the values are restricted to a controlled list.

Controlled List Values:
Code
English
French
CODE1
English Description 1
French Description 1
CODE2
English Description 2
French Description 2

Validation
Indicates what the system will accept in this field
Validation Errors
This section indicates when an error has been made. It will detail the error and provide instruction on how to correct it.
Example Value
Provide one or more real examples of the values that may appear, e.g. “CODE1” or “Family Services Reform Program”
    5.0 Fields
    '''

    p = document.add_paragraph('A plain paragraph having some ')
    p.add_run('bold').bold = True
    p.add_run(' and some ')
    p.add_run('italic.').italic = True

    document.add_heading('Heading, level 1', level=1)
    document.add_paragraph('Intense quote', style='Intense Quote')

    document.add_paragraph(
        'first item in unordered list', style='List Bullet'
    )
    document.add_paragraph(
        'first item in ordered list', style='List Number'
    )


    document.add_page_break()

    document.save(filename)
