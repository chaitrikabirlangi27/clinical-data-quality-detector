
from pathlib import Path
import pyreadstat

from src.config_loader import load_config
from src.rule_engine import run_quality_checks

project_root = Path(__file__).resolve().parents[1]
xpt_path = project_root / "input" / "xpt_files" / "SV.xpt"

df, metadata = pyreadstat.read_xport(str(xpt_path))
config = load_config()

findings = run_quality_checks("SV.xpt", df, config)

print("Dataset: SV.xpt")
print("Rows:", len(df))
print("Columns:", len(df.columns))
print("Total findings:", len(findings))

for finding in findings:
    print(finding)
