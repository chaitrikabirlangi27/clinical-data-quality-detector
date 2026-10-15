
import pandas as pd

from src.outlier_checks import check_outliers

df = pd.DataFrame({
    "USUBJID": ["S001", "S002", "S003", "S004", "S005",
                "S006", "S007", "S008", "S009", "S010"],
    "VALUE": [10, 11, 12, 11, 13, 12, 10, 11, 12, 100]
})

findings = check_outliers(
    "TEST.xpt",
    df,
    numeric_variables=["VALUE"]
)

print("Test dataset rows:", len(df))
print("Total outlier findings:", len(findings))

for finding in findings:
    print(finding)
