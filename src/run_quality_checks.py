
from pathlib import Path
import json

from src.xpt_reader import read_xpt_folder
from src.rule_engine import run_quality_checks
from src.report_generator import generate_excel_report

PROJECT_ROOT = Path(__file__).resolve().parents[1]
INPUT_FOLDER = PROJECT_ROOT / "input" / "xpt_files"
OUTPUT_FOLDER = PROJECT_ROOT / "output"


def main():
    OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

    datasets, read_errors = read_xpt_folder(INPUT_FOLDER)

    all_findings = []

    for filename, dataset_info in datasets.items():
        df = dataset_info["data"]

        findings = run_quality_checks(filename, df)
        all_findings.extend(findings)

        print(
            f"Processed {filename}: "
            f"{len(df)} rows, "
            f"{len(df.columns)} columns, "
            f"{len(findings)} findings"
        )

    report = {
        "total_datasets_loaded": len(datasets),
        "total_read_errors": len(read_errors),
        "total_findings": len(all_findings),
        "read_errors": read_errors,
        "findings": all_findings,
    }
    generate_excel_report()
    report_path = OUTPUT_FOLDER / "quality_check_results.json"

    with report_path.open("w", encoding="utf-8") as file:
        json.dump(report, file, indent=2, default=str)

    print("\n--- QUALITY CHECK SUMMARY ---")
    print("Datasets loaded:", len(datasets))
    print("Files with reading errors:", len(read_errors))
    print("Total findings:", len(all_findings))
    print("Report saved to:", report_path)


if __name__ == "__main__":
    main()
