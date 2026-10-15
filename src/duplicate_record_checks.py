
import pandas as pd


def check_duplicate_records(filename, df):
    """Find exact duplicate rows in a dataset."""

    findings = []

    # Mark repeated rows, keeping the first occurrence unflagged.
    duplicate_mask = df.duplicated(keep="first")

    for row_position in range(len(df)):
        if not duplicate_mask.iloc[row_position]:
            continue

        subject_id = None

        if "USUBJID" in df.columns:
            value = df["USUBJID"].iloc[row_position]

            if not pd.isna(value):
                subject_id = value

        findings.append({
            "issue_id": (
                f"DQ-02-{filename}-row-{row_position + 1}"
            ),
            "dataset": filename,
            "rule_id": "DQ-02",
            "issue_type": "Duplicate Record",
            "variable": "ALL",
            "record_id": row_position + 1,
            "subject_id": subject_id,
            "observed_value": (
                df.iloc[row_position]
                .astype(object)
                .where(df.iloc[row_position].notna(), None)
                .to_dict()
            ),
            "expected_value": "Unique record",
            "severity": "Medium",
            "description": (
                f"Exact duplicate record found at row "
                f"{row_position + 1}. The first occurrence "
                f"is retained and this repeated occurrence "
                f"is flagged."
            ),
            "recommendation": (
                "Review the record to determine whether it "
                "is an unintended duplicate or a valid "
                "repeated clinical measurement."
            ),
            "status": "Open",
        })

    return findings
