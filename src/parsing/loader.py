from pypdf import PdfReader


def extract_text_from_pdf(pdf_path):
    """
    Reads a PDF resume and returns all text.
    """

    reader = PdfReader(pdf_path)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text