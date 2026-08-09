from openpyxl import load_workbook


def extract_xlsx_text(file_path: str) -> str:
    workbook = load_workbook(
        file_path,
        read_only=True,
        data_only=True,
    )

    sheets_text = []

    for sheet in workbook.worksheets:

        rows_text = []

        for row in sheet.iter_rows(values_only=True):

            values = []

            for value in row:

                if value is not None:
                    values.append(str(value))

            if values:
                rows_text.append(" | ".join(values))

        if rows_text:

            sheet_text = (
                f"--- Sheet: {sheet.title} ---\n"
                + "\n".join(rows_text)
            )

            sheets_text.append(sheet_text)

    workbook.close()

    return "\n\n".join(sheets_text)