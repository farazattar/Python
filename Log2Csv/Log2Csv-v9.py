import re
import csv
import os
import sys
from datetime import datetime, timedelta

# --- Settings ---
input_file = "trans1.txt"
# Hard-coded interval in seconds
INTERVAL_SECONDS = 1

# Output filename derived from input filename
base_name = os.path.basename(input_file)
output_file = f"output_{base_name}.csv"

# Flag for including descriptions
include_desc = "-d" in sys.argv

# Regex: data lines start with HH:MM:SS
time_pattern = re.compile(r"^\d{2}:\d{2}:\d{2}")

# Read file once
with open(input_file, "r", encoding="utf-8", errors="ignore") as f:
    lines = f.readlines()

# --- Detect start/end datetimes from the header ---
start_datetime = None
end_datetime = None
dt_regex = re.compile(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}")

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

# --- Parse signal headers with fixed-width fields ---
sig_pattern = re.compile(r"^\s*\d+:\s*(.{12})\s+([A-Z0-9]{4})\s+[A-Z0-9]+\s+(.+?)\s*$")

signal_headers = []
for line in lines:
    m = sig_pattern.match(line)
    if m:
        tag = m.group(1)  # Keep exact spacing (12 chars)
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

# Build CSV header row
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

            # Align column count
            expected_values = len(signal_headers)
            if len(values) < expected_values:
                values = values + [""] * (expected_values - len(values))
            elif len(values) > expected_values:
                values = values[:expected_values]

            row_date = str(current_datetime.date())
            row_time = current_datetime.strftime("%H:%M:%S")
            row_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

            writer.writerow([row_date, row_time, row_datetime] + values)

            current_datetime += timedelta(seconds=INTERVAL_SECONDS)

print(f"✅ Extraction complete! Data with headers saved to {output_file}")
