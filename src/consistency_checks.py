
import pandas as pd


def check_consistency(
    filename,
    df,
    consistency_rules=None,
):
    """
    Check logical relationships between variables.

    Each rule contains:
      - left_column
      - right_column
      - condition: "less_equal", "greater_equal", or "equal"
    """

    findings = []
    consistency_rules = consistency_rules or []

    for rule in consistency_rules:
        left_column = rule["left_column"]
        right_column = rule["right_column"]
        condition = rule["condition"]

        if (
            left_column not in df.columns
            or right_column not in df.columns
        ):
            continue

        for row_position in range(len(df)):
            left_value = df[left_column].iloc[row_position]
            right_value = df[right_column].iloc[row_position]

            # Missing values are handled by DQ-01.
            if pd.isna(left_value) or pd.isna(right_value):
                continue

            try:
                if condition == "less_equal":
                    consistent = left_value <= right_value
                    expected = f"{left_column} <= {right_column}"

                elif condition == "greater_equal":
                    consistent = left_value >= right_value
                    expected = f"{left_column} >= {right_column}"

                elif condition == "equal":
                    consistent = left_value == right_value
                    expected = f"{left_column} == {right_column}"

                else:
                    # Unsupported conditions are not evaluated.
                    continue

            except (TypeError, ValueError):
                continue

            if consistent:
                continue

            subject_id = None
            if "USUBJID" in df.columns:
                value = df["USUBJID"].iloc[row_position]
                if not pd.isna(value):
                    subject_id = value

            findings.append({
                "issue_id": (
                    f"DQ-07-{filename}-{left_column}-"
                    f"{right_column}-row-{row_position + 1}"
                ),
                "dataset": filename,
                "rule_id": "DQ-07",
                "issue_type": "Cross-Variable Inconsistency",
                "variable": f"{left_column}, {right_column}",
                "record_id": row_position + 1,
                "subject_id": subject_id,
                "observed_value": {
                    left_column: left_value,
                    right_column: right_value,
                },
                "expected_value": expected,
                "severity": "Medium",
                "description": (
                    f"Values of '{left_column}' and "
                    f"'{right_column}' violate the configured "
                    "consistency rule."
                ),
                "recommendation": (
                    "Review both values against the applicable "
                    "study-specific consistency requirements."
                ),
                "status": "Open",
            })

    return findings
