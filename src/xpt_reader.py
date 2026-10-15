
from pathlib import Path
import pandas as pd
import pyreadstat


def read_xpt_file(file_path):
    """Read one XPT file and return its data and metadata."""

    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    if file_path.suffix.lower() != ".xpt":
        raise ValueError("The input file must have an .xpt extension.")

    if file_path.stat().st_size == 0:
        raise ValueError(f"The XPT file is empty: {file_path.name}")

    df, metadata = pyreadstat.read_xport(file_path)

    return df, metadata


def read_xpt_folder(folder_path):
    """Read all XPT files in a folder and collect their results."""

    folder_path = Path(folder_path)

    if not folder_path.exists():
        raise FileNotFoundError(
            f"Input folder not found: {folder_path}"
        )

    if not folder_path.is_dir():
        raise NotADirectoryError(
            f"Expected a folder: {folder_path}"
        )

    xpt_files = sorted(folder_path.glob("*.xpt"))

    results = {}
    errors = []

    for file_path in xpt_files:
        try:
            df, metadata = read_xpt_file(file_path)

            results[file_path.name] = {
                "data": df,
                "metadata": metadata,
                "row_count": len(df),
                "column_count": len(df.columns),
            }

        except Exception as error:
            errors.append({
                "filename": file_path.name,
                "error": str(error),
            })

    return results, errors
