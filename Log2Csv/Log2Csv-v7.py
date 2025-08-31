import re
import csv
import os
from datetime import datetime, timedelta

# --- Settings ---
input_file = "trans1.txt"
# Hard-coded interval in seconds; change as needed (e.g., 1, 5, 10, 60, ...)
INTERVAL_SECONDS = 1

# Output filename derived from input filename
base_name = os.path.basename(input_file)
output_file = f"output_{base_name}.csv"

# Regex: data lines start with HH:MM:SS
time_pattern = re.compile(r"^\d{2}:\d{2}:\d{2}")

# Read file once
with open(input_file, "r", encoding="utf-8", errors="ignore") as f:
    lines = f.readlines()

# --- Detect start/end datetimes from the header ---
start_datetime = None
end_datetime = None

# Prefer a line that mentions the sequence; otherwise, take the first line with two datetimes
dt_regex = re.compile(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}")
for line in lines:
    if "Sequence of" in line:
        matches = dt_regex.findall(line)
        if len(matches) >= 2:
            start_datetime = datetime.strptime(matches[0], "%Y-%m-%d %H:%M:%S")
            end_datetime   = datetime.strptime(matches[1], "%Y-%m-%d %H:%M:%S")
            break

if not start_datetime or not end_datetime:
    for line in lines:
        matches = dt_regex.findall(line)
        if len(matches) >= 2:
            start_datetime = datetime.strptime(matches[0], "%Y-%m-%d %H:%M:%S")
            end_datetime   = datetime.strptime(matches[1], "%Y-%m-%d %H:%M:%S")
            break

if not start_datetime or not end_datetime:
    raise ValueError("❌ Could not detect start and end times in the log file.")

current_datetime = start_datetime

# --- Parse signal headers with fixed-width fields ---
# Expected layout example:
#  " 1: 30BXY00CE901         XQ01  3C  GENERATOR MW"
#  " 2: 30AI   BXY06         XQ01  3C  GT POWER FACTOR"
#
# Capture:
#   group1: TAG (exactly 12 chars, may include spaces, e.g., '30AI   BXY06')
#   group2: SUFFIX (exactly 4 chars, e.g., 'XQ01')
#   skip   one alphanum token (e.g., '3C')
#   group3: DESCRIPTION (rest of line)
sig_pattern = re.compile(r"^\s*\d+:\s*(.{12})\s+([A-Z0-9]{4})\s+[A-Z0-9]+\s+(.+?)\s*$")

signal_headers = []
for line in lines:
    m = sig_pattern.match(line)
    if m:
        tag = m.group(1)  # DO NOT strip: preserves internal spaces (12-char tag)
        suffix = m.group(2)

        signal_headers.append(f"{tag}-{suffix} ")

# Build CSV header row
headers = ["Date", "Time", "DateTime"] + signal_headers

# --- Write CSV ---
with open(output_file, "w", newline="", encoding="utf-8") as f_out:
    writer = csv.writer(f_out)
    writer.writerow(headers)

    for line in lines:
        line = line.strip()
        if time_pattern.match(line):
            # Stop if we've gone past the end time
            if current_datetime > end_datetime:
                break

            # Split numeric values from the log line (skip the first token HH:MM:SS)
            parts = re.split(r"\s+", line)
            values = parts[1:]

            # Ensure column count matches headers (pad or truncate if needed)
            expected_values = len(signal_headers)
            if len(values) < expected_values:
                values = values + [""] * (expected_values - len(values))
            elif len(values) > expected_values:
                values = values[:expected_values]

            row_date = str(current_datetime.date())
            row_time = current_datetime.strftime("%H:%M:%S")
            row_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

            writer.writerow([row_date, row_time, row_datetime] + values)

            # Advance by fixed interval
            current_datetime += timedelta(seconds=INTERVAL_SECONDS)

print(f"✅ Extraction complete! Data with headers saved to {output_file}")
