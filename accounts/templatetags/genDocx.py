from django import template
from docxtpl import DocxTemplate


register = template.Library()


@register.simple_tag()
def bedTable(name, nIb, date):
    doc = DocxTemplate("bedTablet.docx")
    doc.render({
        "full_name": name,
        "id": nIb,
        "date": date
    })
    doc.save(f"{nIb}.docx")
