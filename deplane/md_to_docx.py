from markdown import markdown as md
from lxml import etree
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls


def insert_markdown(document, markdown):
    """
    Insert markdown into docx document, best effort conversion
    """
    html = md(
        markdown,
        extensions=['tables'],
    )
    root = etree.HTML(html)

    for element in root[0]:
        if element.tag == 'h1':
            document.add_heading(element.text, 1)
        elif element.tag == 'h2':
            document.add_heading(element.text, 2)
        elif element.tag == 'h3':
            document.add_heading(element.text, 3)
        elif element.tag == 'p':
            if element.text.strip():
                document.add_paragraph(element.text.strip())
        elif element.tag == 'ul':
            for li in element:
                document.add_paragraph(li.text, style='List Paragraph')
        elif element.tag == 'table':
            thead = element[0]
            table = document.add_table(rows=0, cols=len(thead[0]))
            for td, cell in zip(thead[0], table.add_row().cells):
                cell.text = td.text

            tbody = element[1]
            for tr in tbody:
                for td, cell in zip(tr, table.add_row().cells):
                    cell.text = td.text

            format_table(table, top_color='d9d9d9')

        else:
            assert 0, element.tag


def format_table(table, widths=None, top_color=None, left_color=None):
    if widths:
        # for Word
        for row in table.rows:
            for i, w in enumerate(widths):
                row.cells[i].width = w
        # for Libreoffice
        for i, w in enumerate(widths):
            table.columns[i].width = w

    if left_color:
        for cell in table.columns[0].cells:
            element = parse_xml(r'<w:shd {} w:fill="{}"/>'.format(nsdecls('w'), left_color))
            cell._tc.get_or_add_tcPr().append(element)

    if top_color:
        for cell in table.rows[0].cells:
            element = parse_xml(r'<w:shd {} w:fill="{}"/>'.format(nsdecls('w'), top_color))
            cell._tc.get_or_add_tcPr().append(element)
