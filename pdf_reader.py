from pypdf import PdfReader


def extract_text(pdf_file):

    text = ""

    try:

        reader = PdfReader(pdf_file)

        for page in reader.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    except Exception:

        return ""

    return text