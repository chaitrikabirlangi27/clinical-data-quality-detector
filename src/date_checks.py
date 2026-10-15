
import pandas as pd


def check_date_chronology(
    filename,
    df,
    date_columns=None,
    date_pairs=None,
):
    """
    Validate configured date columns and date sequences.

    date_columns:
        Columns that should contain parseable dates.

    date_pairs:
        List of (start_date_column, end_date_column) pairs.
    """

    findings = []
    date_columns = date_columns or []
    date_pairs = date_pairs or []

    def add_finding(
        column,
        row_position,
        observed_value,
        expected_value,
        description,
    ):
        subject_id = None

        if "USUBJID" in df.columns:
            value = df["USUBJID"].iloc[row_position]

            if not pd.isna(value):
                subject_id = value

        findings.append({
            "issue_id": (
                f"DQ-06-{filename}-{column}-row-{row_position + 1}"
            ),
            "dataset": filename,
            "rule_id": "DQ-06",
            "issue_type": "Date/Chronology Violation",
            "variable": column,
            "record_id": row_position + 1,
            "subject_id": subject_id,
            "observed_value": str(observed_value),
            "expected_value": expected_value,
            "severity": "Medium",
            "description": description,
            "recommendation": (
                "Verify the date against the source data and "
                "applicable study-specific chronology rules."
            ),
            "status": "Open",
        })

    # Check whether configured dates can be parsed.
    for column in date_columns:
        if column not in df.columns:
            continue

        for row_position, value in enumerate(df[column]):
            # Missing values are handled by DQ-01.
            if pd.isna(value) or str(value).strip() == "":
                continue

            parsed_date = pd.to_datetime(value, errors="coerce")

            if pd.isna(parsed_date):
                add_finding(
                    column,
                    row_position,
                    value,
                    "A parseable date",
                    f"Value '{value}' in '{column}' "
                    "could not be parsed as a date.",
                )

    # Check that each configured end date is not before its start date.
    for start_column, end_column in date_pairs:
        if (
            start_column not in df.columns
            or end_column not in df.columns
        ):
            continue

        for row_position in range(len(df)):
            start_value = df[start_column].iloc[row_position]
            end_value = df[end_column].iloc[row_position]

            # Missing dates are handled separately by DQ-01.
            if (
                pd.isna(start_value)
                or pd.isna(end_value)
                or str(start_value).strip() == ""
                or str(end_value).strip() == ""
            ):
                continue

            start_date = pd.to_datetime(
                start_value, errors="coerce"
            )
            end_date = pd.to_datetime(
                end_value, errors="coerce"
            )

            # Invalid dates are already handled above.
            if pd.isna(start_date) or pd.isna(end_date):
                continue

            if end_date < start_date:
                add_finding(
                    end_column,
                    row_position,
                    end_value,
                    f"Date on or after {start_column}",
                    f"'{end_column}' occurs before "
                    f"'{start_column}' in this record.",
                )

    return findings
