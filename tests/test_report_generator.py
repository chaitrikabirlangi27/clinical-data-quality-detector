
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.report_generator import generate_excel_report


report_path = generate_excel_report()

print("Excel report exists:", report_path.exists())
