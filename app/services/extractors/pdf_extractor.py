import fitz


def extract_pdf_text(file_path: str) -> str:
    document = fitz.open(file_path)

    pages = []

    for page in document:
        text = page.get_text().strip()

        if text:
            pages.append(text)

    document.close()

    return "\n".join(pages)