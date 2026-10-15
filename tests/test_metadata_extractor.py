
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from xpt_reader import read_xpt_folder
from metadata_extractor import extract_dataset_metadata

INPUT_FOLDER = PROJECT_ROOT / "input" / "xpt_files"

datasets, errors = read_xpt_folder(INPUT_FOLDER)

dataset_summaries = []
variable_summaries = []

for filename, result in datasets.items():
    dataset_summary, variable_summary = extract_dataset_metadata(
        filename,
        result["data"],
        result["metadata"],
    )

    dataset_summaries.append(dataset_summary)
    variable_summaries.extend(variable_summary)

print("========== METADATA EXTRACTOR TEST ==========")
print(f"Datasets processed: {len(dataset_summaries)}")
print(f"Variable summaries created: {len(variable_summaries)}")
print(f"File reading errors: {len(errors)}")

print("\nDataset summaries:")
for summary in dataset_summaries:
    print(summary)

print("\nFirst 10 variable summaries:")
for summary in variable_summaries[:10]:
    print(summary)
