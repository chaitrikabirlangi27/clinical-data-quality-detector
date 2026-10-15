
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.xpt_reader import read_xpt_file


project_root = Path(__file__).resolve().parents[1]
sv_path = project_root / "input" / "xpt_files" / "SV.xpt"

df, metadata = read_xpt_file(sv_path)

duplicate_mask = df.duplicated(keep="first")

print("Total rows:", len(df))
print("Exact duplicate rows:", int(duplicate_mask.sum()))

for position in range(len(df)):
    if not duplicate_mask.iloc[position]:
        continue

    current_row = df.iloc[position]

    # Find earlier rows that match every column.
    earlier_matches = df.iloc[:position].eq(current_row).all(axis=1)
    matching_positions = [
        int(index) + 1
        for index in df.index[:position][earlier_matches]
    ]

    print(
        f"Duplicate row {position + 1} "
        f"matches earlier row(s): {matching_positions}"
    )
    print("Subject:", current_row.get("USUBJID"))
    print("Visit:", current_row.get("VISIT"))
