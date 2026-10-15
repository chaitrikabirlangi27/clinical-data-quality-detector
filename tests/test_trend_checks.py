
import pandas as pd

from src.trend_checks import check_subject_trends

df = pd.DataFrame({
    "USUBJID": ["S001", "S001", "S001", "S002", "S002"],
    "SEQ": [1, 2, 3, 1, 2],
    "VALUE": [10, 12, 50, 20, 22]
})

findings = check_subject_trends(
    "TEST.xpt",
    df,
    measurement_thresholds={"VALUE": 20},
    subject_column="USUBJID",
    sequence_column="SEQ"
)

print("Test dataset rows:", len(df))
print("Total findings:", len(findings))

for finding in findings:
    print(finding)
