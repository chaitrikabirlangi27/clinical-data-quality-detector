
from src.config_loader import load_config
from src.missing_value_checks import check_missing_values
from src.duplicate_record_checks import check_duplicate_records
from src.outlier_checks import check_outliers
from src.range_checks import check_range_and_allowed_values
from src.trend_checks import check_subject_trends
from src.date_checks import check_date_chronology
from src.consistency_checks import check_consistency
from src.sdtm_checks import check_sdtm_compliance


def run_quality_checks(filename, df, config=None):
    """Run configured quality checks on one dataset."""

    if config is None:
        config = load_config()

    findings = []

    # DQ-01: Missing values
    rules = config.get("missing_value_rules", {})
    findings.extend(check_missing_values(
        filename,
        df,
        required_variables=rules.get("required_variables", {}).get(
            filename, []
        ),
        missing_thresholds=rules.get("missing_thresholds", {}),
    ))

    # DQ-02: Exact duplicate records
    duplicate_rules = config.get("duplicate_record_rules", {})
    if duplicate_rules.get("enabled", True):
        findings.extend(check_duplicate_records(filename, df))

    
    
    # DQ-03: Outliers
    rules = config.get("outlier_rules", {})
    configured_variables = rules.get("numeric_variables", {})
    numeric_variables = configured_variables.get(filename, [])

    # Run outlier detection only when variables are configured.
    if numeric_variables:
        findings.extend(check_outliers(
            filename,
            df,
            numeric_variables=numeric_variables,
        ))


    # DQ-04: Numeric ranges and allowed values
    rules = config.get("range_rules", {})
    findings.extend(check_range_and_allowed_values(
        filename,
        df,
        numeric_ranges=rules.get("numeric_ranges", {}).get(
            filename, {}
        ),
        allowed_values=rules.get("allowed_values", {}).get(
            filename, {}
        ),
    ))

    # DQ-05: Subject-level trends
    rules = config.get("trend_rules", {})
    findings.extend(check_subject_trends(
        filename,
        df,
        measurement_thresholds=rules.get(
            "measurement_thresholds", {}
        ).get(filename, {}),
        sequence_column=rules.get("sequence_column"),
    ))

    
    # DQ-06: Date and chronology
    rules = config.get("date_rules", {})

    date_columns = rules.get("date_columns", [])
    date_pairs = rules.get("date_pairs", [])

    # Support both global lists and dataset-specific dictionaries.
    if isinstance(date_columns, dict):
        date_columns = date_columns.get(filename, [])

    if isinstance(date_pairs, dict):
        date_pairs = date_pairs.get(filename, [])

    findings.extend(check_date_chronology(
        filename,
        df,
        date_columns=date_columns,
        date_pairs=date_pairs,
    ))


    # DQ-07: Cross-variable consistency
    rules = config.get("consistency_rules", [])
    dataset_rules = [
        rule for rule in rules
        if rule.get("dataset") == filename
    ]
    findings.extend(check_consistency(
        filename,
        df,
        consistency_rules=dataset_rules,
    ))

    # DQ-08: SDTM structure and terminology
    rules = config.get("sdtm_rules", {})
    findings.extend(check_sdtm_compliance(
        filename,
        df,
        required_variables=rules.get("required_variables", {}).get(
            filename, []
        ),
        controlled_terminology=rules.get(
            "controlled_terminology", {}
        ).get(filename, {}),
    ))

    return findings
