
import streamlit as st
import pandas as pd
import pyreadstat
import tempfile
from pathlib import Path

from src.rule_engine import run_quality_checks
from src.config_loader import load_config
from src.metadata_extractor import extract_dataset_metadata


st.set_page_config(
    page_title="Clinical Data Quality Detector",
    page_icon="🔬",
    layout="wide"
)

st.title("Clinical Data Quality Detector")
st.write(
    "Upload SAS XPT datasets to inspect their metadata, "
    "run configured data quality checks, and download reports."
)

uploaded_files = st.file_uploader(
    "Upload one or more XPT files",
    type=["xpt"],
    accept_multiple_files=True
)

if uploaded_files:
    if st.button("Run Data Quality Checks"):
        config = load_config()

        all_findings = []
        dataset_summaries = []
        variable_summaries = []
        errors = []

        progress = st.progress(0)

        for index, uploaded_file in enumerate(uploaded_files):
            try:
                with tempfile.TemporaryDirectory() as temp_dir:
                    file_path = Path(temp_dir) / uploaded_file.name
                    file_path.write_bytes(uploaded_file.getvalue())

                    df, metadata = pyreadstat.read_xport(str(file_path))

                    dataset_summary, variable_summary = (
                        extract_dataset_metadata(
                            uploaded_file.name, df, metadata
                        )
                    )

                    dataset_summaries.append(dataset_summary)
                    variable_summaries.extend(variable_summary)

                    findings = run_quality_checks(
                        uploaded_file.name, df, config
                    )
                    all_findings.extend(findings)

                st.success(f"Processed {uploaded_file.name}")

            except Exception as error:
                errors.append({
                    "filename": uploaded_file.name,
                    "error": str(error)
                })
                st.error(f"Could not process {uploaded_file.name}: {error}")

            progress.progress((index + 1) / len(uploaded_files))

        st.session_state["findings"] = all_findings
        st.session_state["dataset_summaries"] = dataset_summaries
        st.session_state["variable_summaries"] = variable_summaries
        st.session_state["errors"] = errors

if "findings" in st.session_state:
    findings = st.session_state["findings"]
    dataset_summaries = st.session_state["dataset_summaries"]
    variable_summaries = st.session_state["variable_summaries"]
    errors = st.session_state["errors"]

    st.divider()
    st.header("Quality Check Results")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Datasets Processed", len(dataset_summaries))
    col2.metric("Variables", len(variable_summaries))
    col3.metric("Findings", len(findings))
    col4.metric("Processing Errors", len(errors))

    st.subheader("Dataset Metadata")
    if dataset_summaries:
        st.dataframe(
            pd.DataFrame(dataset_summaries),
            use_container_width=True
        )

    st.subheader("Variable Metadata")
    if variable_summaries:
        st.dataframe(
            pd.DataFrame(variable_summaries),
            use_container_width=True
        )

    st.subheader("Data Quality Findings")
    if findings:
        st.dataframe(
            pd.DataFrame(findings),
            use_container_width=True
        )
    else:
        st.info(
            "No findings were detected by the currently configured checks."
        )

    if errors:
        st.subheader("Files with Processing Errors")
        st.dataframe(pd.DataFrame(errors), use_container_width=True)

    findings_json = pd.DataFrame(findings).to_json(
        orient="records", indent=2
    )
    st.download_button(
        "Download Findings (JSON)",
        data=findings_json,
        file_name="quality_check_findings.json",
        mime="application/json"
    )

    report_frames = {
        "Dataset Metadata": pd.DataFrame(dataset_summaries),
        "Variable Metadata": pd.DataFrame(variable_summaries),
        "Findings": pd.DataFrame(findings),
        "Processing Errors": pd.DataFrame(errors)
    }

    import io

    excel_buffer = io.BytesIO()
    with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
        for sheet_name, frame in report_frames.items():
            if frame.empty:
                frame = pd.DataFrame({"Message": ["No records"]})
            frame.to_excel(writer, sheet_name=sheet_name, index=False)

    st.download_button(
        "Download Complete Report (Excel)",
        data=excel_buffer.getvalue(),
        file_name="clinical_data_quality_report.xlsx",
        mime=(
            "application/vnd.openxmlformats-officedocument."
            "spreadsheetml.sheet"
        )
    )
