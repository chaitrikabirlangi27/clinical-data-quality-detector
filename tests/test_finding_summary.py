
import json
from collections import Counter
from pathlib import Path


project_root = Path(__file__).resolve().parents[1]
report_path = project_root / "output" / "quality_check_results.json"

with report_path.open("r", encoding="utf-8") as file:
    report = json.load(file)

findings = report["findings"]

rule_counts = Counter(
    finding["rule_id"] for finding in findings
)

dataset_counts = Counter(
    finding["dataset"] for finding in findings
)

print("--- FINDINGS BY RULE ---")
for rule_id, count in sorted(rule_counts.items()):
    print(f"{rule_id}: {count}")

print("\n--- TOP 10 DATASETS BY FINDINGS ---")
for dataset, count in dataset_counts.most_common(10):
    print(f"{dataset}: {count}")

print("\nTotal findings:", len(findings))
