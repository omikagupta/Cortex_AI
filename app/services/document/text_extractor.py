from pathlib import Path


class TextExtractor:

    def extract(self, file_path: str, content_type: str) -> str:
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(
                f"File not found: {file_path}"
            )

        # DOCX
        if content_type == (
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        ):
            return self._extract_docx(path)

        # TXT
        if content_type == "text/plain":
            return path.read_text(
                encoding="utf-8",
                errors="ignore",
            )

        # Unsupported format
        return ""

    def _extract_docx(self, path: Path) -> str:
        from docx import Document

        document = Document(path)

        paragraphs = []

        for paragraph in document.paragraphs:
            text = paragraph.text.strip()

            if text:
                paragraphs.append(text)

        return "\n".join(paragraphs)