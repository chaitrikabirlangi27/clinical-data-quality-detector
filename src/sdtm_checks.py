
import pandas as pd


def check_sdtm_compliance(
    filename,
    df,
    required_variables=None,
    controlled_terminology=None,
):
    """
    Check configured SDTM structure and terminology rules.

    required_variables:
        Variables required in the dataset.

    controlled_terminology:
        Dictionary mapping columns to permitted values.
    """

    findings = []
    required_variables = required_variables or []
    controlled_terminology = controlled_terminology or {}

    # Check whether required variables exist.
    for column in required_variables:
        if column not in df.columns:
            findings.append({
                "issue_id": f"DQ-08-{filename}-missing-column-{column}",
                "dataset": filename,
                "rule_id": "DQ-08",
                "issue_type": "Missing Required Variable",
                "variable": column,
                "record_id": None,
                "subject_id": None,
                "observed_value": None,
                "expected_value": "Required variable present",
                "severity": "High",
                "description": (
                    f"Required variable '{column}' "
                    "is missing from the dataset."
                ),
                "recommendation": (
                    "Verify the dataset structure against the "
                    "applicable SDTM domain specification."
                ),
                "status": "Open",
            })

    # Check configured controlled terminology.
    for column, permitted_values in controlled_terminology.items():
        if column not in df.columns:
            continue

        for row_position, value in enumerate(df[column]):
            # Missing values are handled by DQ-01.
            if pd.isna(value):
                continue

            if value not in permitted_values:
                subject_id = None

                if "USUBJID" in df.columns:
                    subject_value = df["USUBJID"].iloc[row_position]
                    if not pd.isna(subject_value):
                        subject_id = subject_value

                findings.append({
                    "issue_id": (
                        f"DQ-08-{filename}-{column}-"
                        f"row-{row_position + 1}"
                    ),
                    "dataset": filename,
                    "rule_id": "DQ-08",
                    "issue_type": "Controlled Terminology Violation",
                    "variable": column,
                    "record_id": row_position + 1,
                    "subject_id": subject_id,
                    "observed_value": value,
                    "expected_value": permitted_values,
                    "severity": "Medium",
                    "description": (
                        f"Value '{value}' in '{column}' "
                        "is not in the configured terminology."
                    ),
                    "recommendation": (
                        "Verify the value against the applicable "
                        "SDTM controlled terminology and study rules."
                    ),
                    "status": "Open",
                })

    return findings
