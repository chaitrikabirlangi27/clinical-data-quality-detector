
import pandas as pd


def check_range_and_allowed_values(
    filename,
    df,
    numeric_ranges=None,
    allowed_values=None,
):
    """
    Check numeric ranges and allowed categorical values.

    numeric_ranges example:
        {"AGE": {"min": 18, "max": 100}}

    allowed_values example:
        {"SEX": ["M", "F", "U"]}
    """

    findings = []
    numeric_ranges = numeric_ranges or {}
    allowed_values = allowed_values or {}

    def add_finding(column, row_position, observed, expected, description):
        subject_id = None

        if "USUBJID" in df.columns:
            value = df["USUBJID"].iloc[row_position]
            if not pd.isna(value):
                subject_id = value

        findings.append({
            "issue_id": (
                f"DQ-04-{filename}-{column}-row-{row_position + 1}"
            ),
            "dataset": filename,
            "rule_id": "DQ-04",
            "issue_type": "Range/Allowed-Value Violation",
            "variable": column,
            "record_id": row_position + 1,
            "subject_id": subject_id,
            "observed_value": observed,
            "expected_value": expected,
            "severity": "Medium",
            "description": description,
            "recommendation": (
                "Verify the value against the applicable "
                "study-specific rules and source data."
            ),
            "status": "Open",
        })

    # Check configured numeric ranges.
    for column, limits in numeric_ranges.items():
        if column not in df.columns:
            continue

        minimum = limits.get("min")
        maximum = limits.get("max")

        for row_position, value in enumerate(df[column]):
            if pd.isna(value):
                continue

            try:
                numeric_value = float(value)
            except (TypeError, ValueError):
                add_finding(
                    column,
                    row_position,
                    value,
                    "Numeric value",
                    f"Non-numeric value found in '{column}', "
                    "which has a configured numeric range.",
                )
                continue

            below_minimum = (
                minimum is not None and numeric_value < minimum
            )
            above_maximum = (
                maximum is not None and numeric_value > maximum
            )

            if below_minimum or above_maximum:
                add_finding(
                    column,
                    row_position,
                    value,
                    f"Minimum: {minimum}, maximum: {maximum}",
                    f"Value {value} in '{column}' is outside "
                    "the configured numeric range.",
                )

    # Check configured allowed categories.
    for column, permitted_values in allowed_values.items():
        if column not in df.columns:
            continue

        for row_position, value in enumerate(df[column]):
            if pd.isna(value):
                continue

            if value not in permitted_values:
                add_finding(
                    column,
                    row_position,
                    value,
                    permitted_values,
                    f"Value '{value}' in '{column}' is not "
                    "in the configured allowed values.",
                )

    return findings
