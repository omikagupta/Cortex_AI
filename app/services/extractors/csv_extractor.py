import pandas as pd


def extract_csv_text(file_path: str) -> str:

    dataframe = pd.read_csv(file_path)

    if dataframe.empty:
        return ""

    return dataframe.to_csv(
        index=False
    )