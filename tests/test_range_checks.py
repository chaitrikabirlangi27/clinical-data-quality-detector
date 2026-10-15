
import pandas as pd

from src.range_checks import check_range_and_allowed_values

df = pd.DataFrame({
    "USUBJID": ["S001", "S002", "S003", "S004"],
    "AGE": [25, 40, 150, 35],
    "SEX": ["M", "F", "X", "M"]
})

findings = check_range_and_allowed_values(
    "TEST.xpt",
    df,
    numeric_ranges={
        "AGE": {"min": 0, "max": 120}
    },
    allowed_values={
        "SEX": ["M", "F"]
    }
)

print("Test dataset rows:", len(df))
print("Total findings:", len(findings))

for finding in findings:
    print(finding)
