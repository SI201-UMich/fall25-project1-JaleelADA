import csv 
from dataclasses import dataclass
from typing import List, Dict
from pathlib import Path
import sys

# Define path to the CSV file & output directory
CSV_FILE_PATH = Path("crop_yield.csv")
OUTPUT_DIR = Path("out")
OUTPUT_DIR.mkdir(exist_ok=True)

# Data types
Row = Dict[str, str]
CleanRow = Dict[str, object]

# Utility functions
def load_csv_to_dicts(file_path: Path) -> List[Row]:
    """Load CSV file and return a list of dictionaries."""
    with file_path.open(newline='', encoding='utf-8') as f:
        r = csv.DictReader(f)
        return [dict(r) for row in r]