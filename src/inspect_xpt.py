
from pathlib import Path
import pandas as pd
import pyreadstat

# Folder containing the XPT files
INPUT_FOLDER = Path("input/xpt_files")

# Find all XPT files
xpt_files = sorted(INPUT_FOLDER.glob("*.xpt"))

print(f"Total XPT files found: {len(xpt_files)}")
print("=" * 60)

# Inspect each dataset
for file_path in xpt_files:
    print(f"\nDataset: {file_path.name}")

    try:
        df, metadata = pyreadstat.read_xport(file_path)

        print(f"Rows: {df.shape[0]}")
        print(f"Columns: {df.shape[1]}")
        print(f"Variable names: {list(df.columns)}")

        # Display variable labels when available
        print("Variable labels:")
        print(metadata.column_names_to_labels)

        # Count missing values
        print("Missing values per variable:")
        print(df.isna().sum().to_dict())

    except Exception as error:
        print(f"Could not read this file: {error}")

    print("-" * 60)
