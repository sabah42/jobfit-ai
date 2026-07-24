from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO


def creer_pdf(texte):

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    contenu = []

    for ligne in texte.split("\n"):
        contenu.append(
            Paragraph(ligne, styles["BodyText"])
        )

    doc.build(contenu)

    buffer.seek(0)

    return buffer
