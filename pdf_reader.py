from pypdf import PdfReader


def extract_text(pdf_file):
    """
    Extract text from uploaded PDF.
    Returns complete document text.
    """

    text = ""

    try:

        reader = PdfReader(pdf_file)

        for page in reader.pages:

            page_text = page.extract_text()

            if page_text:

                text += page_text + "\n"

    except Exception as e:

        print(f"PDF Reading Error: {e}")

        return ""

    return text


def get_pdf_info(pdf_file):
    """
    Returns PDF metadata.
    """

    try:

        reader = PdfReader(pdf_file)

        return {
            "filename": pdf_file.name,
            "total_pages": len(reader.pages),
            "size_kb": round(
                pdf_file.size / 1024,
                2
            )
        }

    except Exception:

        return {
            "filename": pdf_file.name,
            "total_pages": 0,
            "size_kb": 0
        }