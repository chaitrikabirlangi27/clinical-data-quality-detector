
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pandas as pd
from src.duplicate_record_checks import check_duplicate_records


# Sample data containing one exact duplicate.
df = pd.DataFrame({
    "USUBJID": ["SUB001", "SUB002", "SUB001"],
    "VISIT": ["SCREENING", "SCREENING", "SCREENING"],
    "VALUE": [120, 110, 120],
})

findings = check_duplicate_records("TEST.xpt", df)

print("Total duplicate findings:", len(findings))

for finding in findings:
    print(finding)
