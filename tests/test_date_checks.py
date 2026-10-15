
import pandas as pd

from src.date_checks import check_date_chronology

df = pd.DataFrame({
    "USUBJID": ["S001", "S002", "S003"],
    "START_DATE": [
        "2025-01-10",
        "2025-02-15",
        "2025-03-20"
    ],
    "END_DATE": [
        "2025-01-15",
        "2025-02-10",
        "2025-03-25"
    ]
})

findings = check_date_chronology(
    "TEST.xpt",
    df,
    date_columns=["START_DATE", "END_DATE"],
    date_pairs=[
        ("START_DATE", "END_DATE")
    ]
)

print("Test dataset rows:", len(df))
print("Total findings:", len(findings))

for finding in findings:
    print(finding)
