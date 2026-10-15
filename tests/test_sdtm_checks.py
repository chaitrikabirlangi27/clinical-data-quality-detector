
import pandas as pd

from src.sdtm_checks import check_sdtm_compliance

df = pd.DataFrame({
    "USUBJID": ["S001", "S002", "S003"],
    "SEX": ["M", "F", "X"],
    "AGE": [25, 35, 40]
})

findings = check_sdtm_compliance(
    "TEST.xpt",
    df,
    required_variables=["USUBJID", "SEX", "AGE", "DOMAIN"],
    controlled_terminology={
        "SEX": ["M", "F"]
    }
)

print("Test dataset rows:", len(df))
print("Total findings:", len(findings))

for finding in findings:
    print(finding)
