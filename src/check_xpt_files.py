
from pathlib import Path
import pyreadstat

input_folder = Path("input/xpt_files")
xpt_files = sorted(input_folder.glob("*.xpt"))

readable = 0
empty = []
failed = []

for file_path in xpt_files:
    try:
        df, metadata = pyreadstat.read_xport(file_path)
        readable += 1

        if df.empty:
            empty.append(file_path.name)

    except Exception as error:
        failed.append((file_path.name, str(error)))

print("\n--- XPT FILE VALIDATION SUMMARY ---")
print(f"Total files: {len(xpt_files)}")
print(f"Readable files: {readable}")
print(f"Empty datasets: {len(empty)}")
print(f"Failed files: {len(failed)}")

print("\nEmpty datasets:")
for name in empty:
    print("-", name)

print("\nFiles that could not be read:")
if failed:
    for name, error in failed:
        print(f"- {name}: {error}")
else:
    print("None")
