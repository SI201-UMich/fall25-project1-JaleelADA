import csv 
from dataclasses import dataclass
from typing import List, Dict, Tuple
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
            if key.lower() in {"yield (tons/hectare)", "yield_tons_per_hectare", "rainfall_mm", "rainfall (mm)", "temperature_c" }:
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
        yv = row.get(yield_key)
        if not region or isinstance(yv, str) or yv is None:
            continue
        sums[region] = sums.get(region, 0.0) + yv
        counts[region] = counts.get(region, 0) + 1

    results = []
    for region, total in sums.items():
        c = counts[region]
        if c > 0:
            results.append((region, total / c))

    return sorted(results, key=lambda x: x[0])

# Write average yield by region to CSV
def write_average_yield_by_region(results: List[Tuple[str, float]], output_dir: Path) -> None:
    """Compute percentage of Maize harvests in each region with yield > threshold and write to CSV.
    Uses: Region, Crop, Yield (tons/hectare)
    Returns sorted list of (region, percent_high, high_count, total_count).
    """
    out_path = output_dir / "average_yield_by_region.csv"
    with out_path.open('w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Region', 'Average Yield'])
        for region, avg_yield in results:
            writer.writerow([region, f"{avg_yield:.4f}"])
            
            
#Calculation 2: Percentage of High-Yield Maize Harvests by Region
def percentage_high_yield_maize_by_region(rows: List[CleanRow], threshold: float = 5.0) -> List[Tuple[str, float, int, int]]:
    """
    Compute percentage og Maize harvests in each region with yield > threshold.
    uses Region, Crop, Yield (tons/hectare)
    Returns sorted list of (region, percent_high, high_count, total_count).
    
    """
    totals : Dict[str, int] = {}
    highs: Dict[str, int] = {}
    
    region_key = find_key(rows, ["Region"])
    crop_key = find_key(rows, ["Crop"])
    yield_key = find_key(rows, ["Yield (tons/hectare)", "yield (tons/hectare)", "Yield_tons_per_hectare", "yield_tons_per_hectare"])
    
    for row in rows:
        region = row.get(region_key)
        crop = row.get(crop_key)
        yv = row.get(yield_key)
        
        if not region or not crop or not isinstance(yv, (int, float)) or yv is None:
            continue
        if str(crop).strip().lower() != "maize":
            continue
        totals[region] = totals.get(region, 0) + 1
        if float(yv) > threshold:
            highs[region] = highs.get(region, 0) + 1
            
    results: List[Tuple[str, float, int, int]] = []
    
    for region, total in totals.items():
        high = highs.get(region, 0)
        percent = (high / total) * 100 if total > 0 else 0.0
        results.append((region, percent, high, total))
        
    return sorted(results, key=lambda x: x[0])

def write_percentage_high_yield_maize_by_region(results: List[Tuple[str, float, int, int]], output_dir: Path) -> None:
    """Write text summary of percentage high-yield maize by region to CSV."""
    
    out_path = output_dir / "percentage_high_yield_maize_by_region.txt"
    with out_path.open('w', newline='', encoding='utf-8') as f:
        f.write("Percentage High-Yield Maize Harvests by Region in Tons/Hectare\n")
        f.write('=' * 60 + '\n')
        for region, percent, high, total in results:
            f.write(f"{region:20} {percent:6.2f}% ({high}/{total})\n")


# Helper to find key in row with possible alternatives
def find_key(rows: List[CleanRow], alternatives: List[str]) -> str:
    if not rows:
        return alternatives[0]
    lower_map = {k.lower(): k for k in rows[0].keys()}
    for c in alternatives:
        if c.lower() in lower_map:
            return lower_map[c.lower()]
        
    return alternatives[0]


def main