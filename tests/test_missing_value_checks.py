
import pandas as pd
import sys
from pathlib import Path

# Add the project root folder to Python's import path.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.missing_value_checks import check_missing_values

from src.missing_value_checks import check_missing_values


# Small sample dataset for testing.
df = pd.DataFrame({
    "USUBJID": ["SUB001", "SUB002", None, "SUB004"],
    "AGE": [25, None, 40, None],
    "SEX": ["F", "M", "F", "M"],
})

findings = check_missing_values(
    filename="TEST.xpt",
    df=df,
    required_variables=["USUBJID"],
    missing_thresholds={"AGE": 25},
)

print("Total findings:", len(findings))

for finding in findings:
    print(finding)
