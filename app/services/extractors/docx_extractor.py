from docx import Document


def extract_docx_text(file_path: str) -> str:

    print("DOCX EXTRACTOR CALLED")
    print("Path:", file_path)

    document = Document(file_path)

    extracted_parts = []

    # Paragraphs
    for paragraph in document.paragraphs:

        text = paragraph.text.strip()

        if text:
            extracted_parts.append(text)

    # Tables
    for table in document.tables:

        for row in table.rows:

            row_text = []

            for cell in row.cells:

                cell_text = cell.text.strip()

                if cell_text:
                    row_text.append(cell_text)

            if row_text:
                extracted_parts.append(
                    " | ".join(row_text)
                )

    result = "\n".join(extracted_parts)

    print(
        "DOCX EXTRACTION LENGTH:",
        len(result)
    )

    return result