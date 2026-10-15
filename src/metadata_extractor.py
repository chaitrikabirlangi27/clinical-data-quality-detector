
import pandas as pd


def extract_dataset_metadata(filename, df, metadata):
    """Extract dataset-level and variable-level metadata."""

    dataset_summary = {
        "dataset_name": filename,
        "row_count": len(df),
        "column_count": len(df.columns),
    }

    variable_summaries = []

    for column in df.columns:
        series = df[column]

        variable_summaries.append({
            "dataset_name": filename,
            "variable_name": column,
            "variable_label": (
                metadata.column_names_to_labels.get(column, "")
                if metadata.column_names_to_labels
                else ""
            ),
            "data_type": str(series.dtype),
            "missing_count": int(series.isna().sum()),
            "missing_percentage": (
                round(series.isna().mean() * 100, 2)
                if len(df) > 0
                else 0.0
            ),
            "distinct_values": int(series.nunique(dropna=True)),
            "minimum": series.min() if pd.api.types.is_numeric_dtype(series) else None,
            "maximum": series.max() if pd.api.types.is_numeric_dtype(series) else None,
        })

    return dataset_summary, variable_summaries
