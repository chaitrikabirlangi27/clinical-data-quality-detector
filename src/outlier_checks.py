
import pandas as pd


def check_outliers(filename, df, numeric_variables=None):
    """
    Detect numeric outliers using the IQR method.

    numeric_variables:
        List of numeric columns to check.
        If omitted, all numeric columns are checked.
    """

    findings = []

    if numeric_variables is None:
        numeric_variables = df.select_dtypes(
            include="number"
        ).columns.tolist()

    for column in numeric_variables:
        if column not in df.columns:
            continue

        values = pd.to_numeric(df[column], errors="coerce")
        valid_values = values.dropna()

        # IQR needs enough observations to calculate useful quartiles.
        if len(valid_values) < 4:
            continue

        q1 = valid_values.quantile(0.25)
        q3 = valid_values.quantile(0.75)
        iqr = q3 - q1

        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr

        outlier_mask = (
            values.lt(lower_bound) | values.gt(upper_bound)
        ).fillna(False)

        for row_position in range(len(df)):
            if not outlier_mask.iloc[row_position]:
                continue

            observed_value = float(values.iloc[row_position])

            subject_id = None
            if "USUBJID" in df.columns:
                value = df["USUBJID"].iloc[row_position]
                if not pd.isna(value):
                    subject_id = value

            findings.append({
                "issue_id": (
                    f"DQ-03-{filename}-{column}-"
                    f"row-{row_position + 1}"
                ),
                "dataset": filename,
                "rule_id": "DQ-03",
                "issue_type": "Potential Outlier",
                "variable": column,
                "record_id": row_position + 1,
                "subject_id": subject_id,
                "observed_value": observed_value,
                "expected_value": (
                    f"Within [{lower_bound:.2f}, "
                    f"{upper_bound:.2f}] under the IQR rule"
                ),
                "severity": "Medium",
                "description": (
                    f"Potential outlier in '{column}': "
                    f"{observed_value}. IQR bounds: "
                    f"{lower_bound:.2f} to "
                    f"{upper_bound:.2f}."
                ),
                "recommendation": (
                    "Review the observation against clinical "
                    "context and study-specific rules. "
                    "Do not automatically remove it."
                ),
                "status": "Open",
            })

    return findings
