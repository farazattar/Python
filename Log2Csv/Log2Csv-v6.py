import re
import csv
import os
from datetime import datetime, timedelta

input_file = "Test.txt"

# Create output filename based on input filename
base_name = os.path.basename(input_file)
output_file = f"output_{base_name}.csv"

# Hard-coded interval in seconds (change as needed)
INTERVAL_SECONDS = 1  

# Regex to match lines starting with hh:mm:ss
time_pattern = re.compile(r"^\d{2}:\d{2}:\d{2}")

start_datetime = None
end_datetime = None
current_datetime = None

# First, detect start and end datetime from the header
with open(input_file, "r", encoding="utf-8", errors="ignore") as f_in:
    for line in f_in:
        if "Sequence of" in line:
            # Extract start and end datetimes
            matches = re.findall(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}", line)
            if len(matches) >= 2:
                start_datetime = datetime.strptime(matches[0], "%Y-%m-%d %H:%M:%S")
                end_datetime   = datetime.strptime(matches[1], "%Y-%m-%d %H:%M:%S")
                current_datetime = start_datetime
            break

if not start_datetime or not end_datetime:
    raise ValueError("❌ Could not detect start and end times in the log file.")

with open(input_file, "r", encoding="utf-8", errors="ignore") as f_in, \
     open(output_file, "w", newline="", encoding="utf-8") as f_out:
    
    writer = csv.writer(f_out)

    for line in f_in:
        line = line.strip()
        if time_pattern.match(line):
            parts = re.split(r"\s+", line)

            # Stop if beyond end time
            if current_datetime > end_datetime:
                break

            # Build columns: Date, Time, DateTime + values
            row_date = str(current_datetime.date())
            row_time = current_datetime.strftime("%H:%M:%S")
            row_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

            row = [row_date, row_time, row_datetime] + parts[1:]
            writer.writerow(row)

            # Advance by the fixed interval
            current_datetime += timedelta(seconds=INTERVAL_SECONDS)

print(f"✅ Extraction complete! Data saved to {output_file}")
