from markdown import markdown as md
from lxml import etree

def insert_markdown(document, markdown):
    """
    Insert markdown into docx document, best effort conversion
    """
    html = md(markdown)
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
        else:
            assert 0, element.tag