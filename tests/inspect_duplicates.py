
import json
from pathlib import Path


project_root = Path(__file__).resolve().parents[1]
report_path = project_root / "output" / "quality_check_results.json"

with report_path.open("r", encoding="utf-8") as file:
    report = json.load(file)

duplicate_findings = [
    finding
    for finding in report["findings"]
    if finding["rule_id"] == "DQ-02"
]

print("Total duplicate findings:", len(duplicate_findings))

for finding in duplicate_findings:
    print("\nDataset:", finding["dataset"])
    print("Record row:", finding["record_id"])
    print("Subject:", finding["subject_id"])
    print("Duplicate row values:")
    print(finding["observed_value"])
