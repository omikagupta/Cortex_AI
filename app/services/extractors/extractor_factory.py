from pathlib import Path

from app.services.extractors.docx_extractor import extract_docx_text
from app.services.extractors.pdf_extractor import extract_pdf_text
from app.services.extractors.txt_extractor import extract_txt_text
from app.services.extractors.pptx_extractor import extract_pptx_text
from app.services.extractors.xlsx_extractor import extract_xlsx_text
from app.services.extractors.csv_extractor import extract_csv_text


EXTRACTORS = {
    ".pdf": extract_pdf_text,
    ".docx": extract_docx_text,
    ".txt": extract_txt_text,
    ".pptx": extract_pptx_text,
    ".xlsx": extract_xlsx_text,
    ".csv": extract_csv_text,
}


def get_extractor(filename: str):

    extension = Path(filename).suffix.lower()

    return EXTRACTORS.get(extension)