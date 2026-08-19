from pathlib import Path
from docx import Document


class TextExtractor:

    def extract(
        self,
        file_path: str,
        content_type: str,
    ):

        path = Path(file_path)

        print("TEXT EXTRACTION STARTED")
        print("File:", path)

        # DOCX extraction
        if content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":

            doc = Document(path)

            paragraphs = []

            for paragraph in doc.paragraphs:
                if paragraph.text.strip():
                    paragraphs.append(
                        paragraph.text.strip()
                    )

            text = "\n".join(paragraphs)

            print(
                "Extracted characters:",
                len(text),
            )

            return text


        raise ValueError(
            f"Unsupported file type: {content_type}"
        )