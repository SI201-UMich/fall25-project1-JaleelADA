import csv 
from dataclasses import dataclass
from typing import List, Dict
from pathlib import Path
import sys

# Define path to the CSV file & output directory
CSV_FILE_PATH = Path("data.csv")
OUTPUT_DIR = Path("out")
OUTPUT_DIR.mkdir(exist_ok=True)

