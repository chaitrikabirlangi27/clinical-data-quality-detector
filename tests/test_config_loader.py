
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.config_loader import load_config


config = load_config()

print("Configuration loaded successfully!")
print("Available sections:")

for section in config:
    print("-", section)
