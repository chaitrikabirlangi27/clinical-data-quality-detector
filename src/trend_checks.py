
import pandas as pd


def check_subject_trends(
    filename,
    df,
    measurement_thresholds,
    subject_column="USUBJID",
    sequence_column=None,
):
    """
    Flag large changes between consecutive measurements
    for the same subject.

    measurement_thresholds:
        Maximum allowed absolute change for each variable.

    sequence_column:
        Optional column used to order measurements,
        such as a visit number or collection date.
    """

    findings = []

    if subject_column not in df.columns:
        return findings

    # Keep original row numbers for reporting.
    data = df.copy()
    data["_source_row"] = range(1, len(data) + 1)

    for column, threshold in measurement_thresholds.items():
        if column not in data.columns:
            continue

        data["_numeric_value"] = pd.to_numeric(
            data[column], errors="coerce"
        )

        # A missing subject ID cannot be compared reliably.
        valid_data = data.dropna(subset=[
            subject_column, "_numeric_value"
        ])

        for subject_id, group in valid_data.groupby(
            subject_column, sort=False
        ):
            # Sort by the provided visit/date/sequence column.
            if sequence_column and sequence_column in group.columns:
                group = group.sort_values(
                    sequence_column, kind="stable"
                )

            previous_row = None
            previous_value = None

            for _, current_row in group.iterrows():
                current_value = current_row["_numeric_value"]

                if previous_row is not None:
                    change = abs(current_value - previous_value)

                    if change > threshold:
                        row_number = int(current_row["_source_row"])

                        findings.append({
                            "issue_id": (
                                f"DQ-05-{filename}-{column}-"
                                f"row-{row_number}"
                            ),
                            "dataset": filename,
                            "rule_id": "DQ-05",
                            "issue_type": "Potential Trend Anomaly",
                            "variable": column,
                            "record_id": row_number,
                            "subject_id": subject_id,
                            "observed_value": float(current_value),
                            "expected_value": (
                                f"Absolute change <= {threshold}"
                            ),
                            "severity": "Medium",
                            "description": (
                                f"Measurement for subject '{subject_id}' "
                                f"changed from {previous_value} to "
                                f"{current_value}. Absolute change: "
                                f"{change}, exceeding threshold "
                                f"{threshold}."
                            ),
                            "recommendation": (
                                "Review the measurement sequence, "
                                "collection timing, and applicable "
                                "clinical rules. The change may be valid."
                            ),
                            "status": "Open",
                        })

                previous_row = current_row
                previous_value = current_value

        data.drop(columns=["_numeric_value"], inplace=True, errors="ignore")

    return findings
