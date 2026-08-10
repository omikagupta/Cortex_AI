import zipfile
import xml.etree.ElementTree as ET


WORD_NAMESPACE = "http://purl.oclc.org/ooxml/wordprocessingml/main"


def extract_docx_text(file_path: str) -> str:
    print("DOCX EXTRACTOR CALLED")
    print("Path:", file_path)

    with zipfile.ZipFile(file_path, "r") as archive:

        if "word/document.xml" not in archive.namelist():
            raise ValueError(
                "Invalid DOCX: word/document.xml is missing"
            )

        document_xml = archive.read("word/document.xml")

    root = ET.fromstring(document_xml)

    paragraphs = []

    for paragraph in root.iter(
        f"{{{WORD_NAMESPACE}}}p"
    ):

        text_parts = []

        for text_node in paragraph.iter(
            f"{{{WORD_NAMESPACE}}}t"
        ):

            if text_node.text:
                text_parts.append(text_node.text)

        paragraph_text = "".join(text_parts).strip()

        if paragraph_text:
            paragraphs.append(paragraph_text)

    if not paragraphs:
        raise ValueError(
            "DOCX extraction failed: no text paragraphs found"
        )

    extracted_text = "\n".join(paragraphs)

    print("DOCX EXTRACTION SUCCESSFUL")
    print("Paragraphs:", len(paragraphs))
    print("Text length:", len(extracted_text))

    print("First 200 characters:")
    print(extracted_text[:200])

    return extracted_text