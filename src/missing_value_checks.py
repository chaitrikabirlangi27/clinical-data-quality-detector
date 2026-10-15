
import pandas as pd


def check_missing_values(
    filename,
    df,
    required_variables=None,
    missing_thresholds=None,
):
    """
    Check missing values using configurable rules.

    required_variables:
        Variables that must not contain missing values.

    missing_thresholds:
        Maximum allowed missing percentage for each variable.
    """

    required_variables = required_variables or []
    missing_thresholds = missing_thresholds or {}

    findings = []
    dataset_name = filename

    # Check every variable in the dataset.
    for column in df.columns:
        missing_mask = df[column].isna()
        missing_count = int(missing_mask.sum())

        if missing_count == 0:
            continue

        missing_percentage = (
            round((missing_count / len(df)) * 100, 2)
            if len(df) > 0
            else 0.0
        )

        is_required = column in required_variables

        threshold = missing_thresholds.get(column)
        exceeds_threshold = (
            threshold is not None
            and missing_percentage > threshold
        )

        # Report missing values only when a configured rule is violated.
        if not is_required and not exceeds_threshold:
            continue

        for row_position in range(len(df)):
            if not missing_mask.iloc[row_position]:
                continue

            subject_id = None
            if "USUBJID" in df.columns:
                subject_id = df["USUBJID"].iloc[row_position]

                if pd.isna(subject_id):
                    subject_id = None

            findings.append({
                "issue_id": (
                    f"DQ-01-{dataset_name}-{column}-"
                    f"row-{row_position + 1}"
                ),
                "dataset": dataset_name,
                "rule_id": "DQ-01",
                "issue_type": "Missing Value",
                "variable": column,
                "record_id": row_position + 1,
                "subject_id": subject_id,
                "observed_value": None,
                "expected_value": "Non-missing value",
                "severity": "High" if is_required else "Medium",
                "description": (
                    f"Missing value found in '{column}'. "
                    f"Missing count: {missing_count}; "
                    f"missing percentage: {missing_percentage}%."
                ),
                "recommendation": (
                    "Review the source data and applicable "
                    "study-specific data quality rules."
                ),
                "status": "Open",
            })

    return findings
  