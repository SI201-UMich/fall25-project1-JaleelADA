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
    """Convert numeric fields to appropriate types. Skip rows with invalid data."""
    cleaned: List[CleanRow] = []
    for row in rows:
        new = {}
        for key, value in row.items():
            key = key.strip()
            value = value.strip()
            #Attemp numeric coercion
            if key.lower()  {"yield (tons/hectare)", "yield_tons_per_hectare", "rainfall_mm", "rainfall (mm)", "temperature_c" }:
                try:
                    new[key] = float(value) if value else None
                except ValueError:
                    new[key] = None
            else:
                new[key] = value
        cleaned.append(new)
    return cleaned
                
                    
                    
# Calculation 1: Average Yield by Region
def average_yield_by_region(rows: List[CleanRow]) -> List[Tuple[str, float]]:
    """
    Calculate average crop yield for each region (across all crops).
    Uses: Region, Crop, Yield (tons/hectare)
    Returns sorted list of (region, average_yield).
    """
    sums: Dict[str, float] = {}
    counts: Dict[str, int] = {}
    
    region_key = find_key(rows, ["Region"])
    yield_key = find_key(rows, ["Yield (tons/hectare)", "yield (tons/hectare)", "Yield_tons_per_hectare", "yield_tons_per_hectare"])

    for row in rows:
        region = row.get(region_key)
        yv = 