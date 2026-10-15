
import pandas as pd

from src.consistency_checks import check_consistency

df = pd.DataFrame({
    "USUBJID": ["S001", "S002", "S003"],
    "START_AGE": [20, 35, 40],
    "END_AGE": [25, 30, 45]
})

consistency_rules = [
    {
        "dataset": "TEST.xpt",
        "left_column": "END_AGE",
        "right_column": "START_AGE",
        "condition": "greater_equal"
    }
]

findings = check_consistency(
    "TEST.xpt",
    df,
    consistency_rules=consistency_rules
)

print("Test dataset rows:", len(df))
print("Total findings:", len(findings))

for finding in findings:
    print(finding)
