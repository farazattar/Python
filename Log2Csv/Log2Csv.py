import re
import csv
import os
import sys
from datetime import datetime, timedelta

def print_help():
    help_text = """
Usage:
  python Log2Csv.py <input_file> [-d] [-o <output_file>] [-i <interval_seconds>] [-h]

Arguments:
  <input_file>         The log file to process (e.g., Test.txt).

Options:
  -d                   Include signal descriptions in the header row.
                       Example: "30BXY00CE901-XQ01 [GENERATOR MW]"
                       Default (without -d): "30BXY00CE901-XQ01"

  -o <output_file>     Specify the output CSV filename.
                       Default: "output_<input_file>.csv"
                       Example: -o mydata.csv

  -i <interval>        Set the sampling interval in seconds.
                       Default: 1
                       Example: -i 5

  -h                   Show this help message and exit.

Examples:
  python Log2Csv.py Test.txt
      → Processes Test.txt, 1-second interval, no descriptions.
         Output: output_Test.txt.csv

  python Log2Csv.py Test.txt -d
      → Processes Test.txt with descriptions in headers.
         Output: output_Test.txt.csv

  python Log2Csv.py Test.txt -i 5 -o data.csv
      → Processes Test.txt, interval = 5 seconds, saves to data.csv

  python Log2Csv.py -h
      → Shows this help message
"""
    print(help_text.strip())

# --- Handle arguments ---
if len(sys.argv) < 2 or "-h" in sys.argv:
    print_help()
    sys.exit(0)

input_file = sys.argv[1]
include_desc = "-d" in sys.argv

# Default output filename
base_name = os.path.basename(input_file)
output_file = f"output_{base_name}.csv"

# Default interval (1 second if -i not provided)
INTERVAL_SECONDS = 1

# Parse -o argument
if "-o" in sys.argv:
    try:
        output_index = sys.argv.index("-o")
        output_file = sys.argv[output_index + 1]
    except IndexError:
        print("❌ Error: -o option requires a filename")
        sys.exit(1)

# Parse -i argument
if "-i" in sys.argv:
    try:
        interval_index = sys.argv.index("-i")
        INTERVAL_SECONDS = int(sys.argv[interval_index + 1])
    except (IndexError, ValueError):
        print("❌ Error: -i option requires an integer (seconds)")
        sys.exit(1)

# Regex patterns
time_pattern = re.compile(r"^\d{2}:\d{2}:\d{2}")
dt_regex = re.compile(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}")
sig_pattern = re.compile(r"^\s*\d+:\s*(.{12})\s+([A-Z0-9]{4})\s+[A-Z0-9]+\s+(.+?)\s*$")

# Read file
with open(input_file, "r", encoding="utf-8", errors="ignore") as f:
    lines = f.readlines()

# --- Detect start/end datetime ---
start_datetime = None
end_datetime = None

for line in lines:
    if "Sequence of" in line:
        matches = dt_regex.findall(line)
        if len(matches) >= 2:
            start_datetime = datetime.strptime(matches[0], "%Y-%m-%d %H:%M:%S")
            end_datetime   = datetime.strptime(matches[1], "%Y-%m-%d %H:%M:%S")
            break

if not start_datetime or not end_datetime:
    raise ValueError("❌ Could not detect start and end times in the log file.")

current_datetime = start_datetime

# --- Parse signal headers ---
signal_headers = []
for line in lines:
    m = sig_pattern.match(line)
    if m:
        tag = m.group(1)  # Keep exact 12 characters (spaces preserved)
        suffix = m.group(2)
        desc = m.group(3)

        # Clean description
        desc = re.sub(r"\s+", " ", desc).strip()
        tokens = desc.split()
        while len(tokens) >= 2 and tokens[-1] == tokens[-2]:
            tokens.pop()
        desc = " ".join(tokens)

        if include_desc:
            signal_headers.append(f"{tag}-{suffix} [{desc}]")
        else:
            signal_headers.append(f"{tag}-{suffix}")

# Build header row
headers = ["Date", "Time", "DateTime"] + signal_headers

# --- Write CSV ---
with open(output_file, "w", newline="", encoding="utf-8") as f_out:
    writer = csv.writer(f_out)
    writer.writerow(headers)

    for line in lines:
        line = line.strip()
        if time_pattern.match(line):
            if current_datetime > end_datetime:
                break

            parts = re.split(r"\s+", line)
            values = parts[1:]

            # Align with header column count
            expected_values = len(signal_headers)
            if len(values) < expected_values:
                values += [""] * (expected_values - len(values))
            elif len(values) > expected_values:
                values = values[:expected_values]

            row_date = str(current_datetime.date())
            row_time = current_datetime.strftime("%H:%M:%S")
            row_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

            writer.writerow([row_date, row_time, row_datetime] + values)

            # Advance time by fixed interval
            current_datetime += timedelta(seconds=INTERVAL_SECONDS)

print(f"✅ Extraction complete! Interval={INTERVAL_SECONDS}s. Data saved to {output_file}")
