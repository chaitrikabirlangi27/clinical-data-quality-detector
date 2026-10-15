
# Clinical Data Quality Detector

## 1. Project Overview

The Clinical Data Quality Detector is a Python-based application that analyzes clinical datasets stored in SAS Transport (XPT) format.

It allows users to upload one or more XPT files, inspect dataset and variable metadata, execute configurable data quality checks, and download the results as JSON and Excel reports.

The goal is to help identify potential data-quality issues and make clinical dataset review easier.

## 2. Problem Statement

Clinical datasets may contain duplicate records, missing values, invalid values, inconsistent variable relationships, and date chronology problems.

Manually reviewing large datasets can be time-consuming. This project automates configurable data-quality checks and generates reports that help users investigate potential issues.

## 3. Objectives

- Read clinical datasets in SAS XPT format.
- Extract dataset and variable metadata.
- Calculate row counts, column counts, missing-value statistics, and distinct-value counts.
- Execute configurable data-quality checks.
- Display findings in an interactive web interface.
- Generate downloadable JSON and Excel reports.

## 4. Technologies Used

- Python
- Pandas
- Pyreadstat
- Streamlit
- NumPy
- OpenPyXL
- JSON
- SAS XPT files

## 5. System Workflow

1. The user uploads one or more XPT files.
2. The application reads each dataset.
3. Dataset and variable metadata are extracted.
4. Configured data-quality checks are executed.
5. Findings and processing errors are collected.
6. Results are displayed in the Streamlit interface.
7. Users download JSON findings or a complete Excel report.

## 6. Data Quality Checks

The project contains eight configurable check implementations.

| Rule ID | Check | Purpose |
|---|---|---|
| DQ-01 | Missing Values | Detect missing values in configured required variables or variables exceeding configured missingness thresholds. |
| DQ-02 | Duplicate Records | Identify exact duplicate records. |
| DQ-03 | Outlier Detection | Identify potential numeric outliers using the IQR method. |
| DQ-04 | Range and Allowed Values | Detect values outside configured numeric ranges or allowed-value lists. |
| DQ-05 | Subject-Level Trends | Identify configured measurement changes exceeding specified thresholds. |
| DQ-06 | Date and Chronology | Check date parsing and configured start/end date relationships. |
| DQ-07 | Cross-Variable Consistency | Check configured logical relationships between variables. |
| DQ-08 | SDTM Structure and Terminology | Check configured required variables and controlled terminology. |

The checks use configurable rules. Their results depend on the rules enabled for each dataset. Potential findings should be reviewed against the applicable study specifications and source data.

## 7. Metadata Profiling

The application displays dataset metadata, including:

- Dataset name
- Number of rows
- Number of columns

Variable metadata includes:

- Variable name and label
- Data type
- Missing-value count and percentage
- Number of distinct values
- Minimum and maximum values for numeric variables

## 8. Reports

### JSON Report

Contains structured data-quality findings for further processing or integration.

### Excel Report

The batch report includes:

- Summary
- Findings by Rule
- Findings by Dataset
- Findings

The Streamlit upload interface also provides a complete Excel report containing dataset metadata, variable metadata, findings, and processing errors.

## 9. Project Structure

```text
clinical_data_quality_detector_project/
├── config/
│   └── domain_rules.json
├── input/
│   └── xpt_files/
├── output/
├── src/
│   ├── app.py
│   ├── config_loader.py
│   ├── consistency_checks.py
│   ├── date_checks.py
│   ├── duplicate_record_checks.py
│   ├── metadata_extractor.py
│   ├── missing_value_checks.py
│   ├── outlier_checks.py
│   ├── range_checks.py
│   ├── report_generator.py
│   ├── rule_engine.py
│   ├── run_quality_checks.py
│   ├── sdtm_checks.py
│   ├── trend_checks.py
│   └── xpt_reader.py
├── tests/
├── requirements.txt
└── README.md
```

## 10. Installation

### Prerequisites

- Python 3.12 or a compatible Python version
- pip

### Create and activate a virtual environment

Windows:

```powershell
python -m venv venv
.\venv\Scripts\activate
```

### Install dependencies

```powershell
pip install -r requirements.txt
```

If Streamlit is not included in the requirements file, install it with:

```powershell
pip install streamlit
```

## 11. Run the Application

From the project root directory, run:

```powershell
python -m streamlit run src/app.py
```

Open the local URL displayed in the terminal, usually:

```text
http://localhost:8501
```

Upload one or more XPT files and click **Run Data Quality Checks**.

## 12. Run Batch Processing

To process the XPT files stored in the configured input folder and generate batch reports, run:

```powershell
python -m src.run_quality_checks
```

The generated reports are saved in the `output/` directory.

## 13. Run Tests

Run individual test modules from the project root, for example:

```powershell
python -m tests.test_xpt_reader
python -m tests.test_rule_engine
python -m tests.test_duplicate_record_checks
python -m tests.test_outlier_checks
python -m tests.test_range_checks
python -m tests.test_trend_checks
python -m tests.test_date_checks
python -m tests.test_consistency_checks
python -m tests.test_sdtm_checks
```

## 14. Current Validation Results

In the current local batch-processing run:

- 35 XPT datasets were loaded.
- No file-reading errors were reported.
- 16 data-quality findings were generated.
- All 16 findings came from exact duplicate records detected in `SV.xpt`.

Individual check modules have also been tested with constructed test datasets. These results demonstrate the tested behaviors; they do not establish that every clinical rule has been validated for every study.

## 15. Limitations

- Findings depend on the configured rules.
- Clinical validity must be reviewed against study-specific requirements.
- An exact duplicate is a potential issue, not automatically an invalid clinical record.
- Outlier thresholds and allowed values must be selected appropriately for the dataset.
- The application identifies potential issues; it does not automatically correct clinical data.

## 16. Future Enhancements

- Configure and validate additional dataset-specific rules.
- Improve Excel report formatting and summaries.
- Add more automated tests for edge cases.
- Enhance error handling and user guidance.
- Add optional explanations of findings.

## 17. Disclaimer

This project is intended for educational and data-quality review purposes. It is not a substitute for validated clinical data-management procedures or formal regulatory compliance review.
