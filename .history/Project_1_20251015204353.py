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
        reader = csv.DictReader(f)
        return [dict(row) for row in reader]

def coerce_types(rows: List[Row]) -> List[CleanRow]:
    """Coerce types of fields in the rows."""
    coerced = []
    for row in rows:
        clean_row: CleanRow = {}
        for key, value in row.items():
            if key == "year":
                clean_row[key] = int(value)
            elif key == "yield":
                clean_row[key] = float(value)
            else:
                clean_row[key] = value
        coerced.append(clean_row)
    return coerced