
from pathlib import Path
import sys

# Allow Python to import modules from the src folder
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from xpt_reader import read_xpt_folder

# Location of the XPT datasets
INPUT_FOLDER = PROJECT_ROOT / "input" / "xpt_files"

# Read all XPT files
datasets, errors = read_xpt_folder(INPUT_FOLDER)

print("========== XPT READER TEST ==========")
print(f"Total datasets loaded: {len(datasets)}")
print(f"Files with errors: {len(errors)}")

print("\nDataset summary:")

for filename, result in datasets.items():
    print(
        f"{filename}: "
        f"{result['row_count']} rows, "
        f"{result['column_count']} columns"
    )

if errors:
    print("\nFiles with errors:")

    for error in errors:
        print(f"{error['filename']}: {error['error']}")
else:
    print("\nAll XPT files were read successfully.")
