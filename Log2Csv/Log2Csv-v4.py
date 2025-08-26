import re
import csv
from datetime import datetime, timedelta

input_file = "Test.txt"
output_file = "output.csv"

# Regex to match lines starting with hh:mm:ss
time_pattern = re.compile(r"^\d{2}:\d{2}:\d{2}")

start_datetime = None
end_datetime = None
current_date = None
previous_time = None

# First, detect start and end datetime from the header
with open(input_file, "r", encoding="utf-8", errors="ignore") as f_in:
    for line in f_in:
        if "Sequence of" in line:
            # Extract start and end datetimes
            matches = re.findall(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}", line)
            if len(matches) >= 2:
                start_datetime = datetime.strptime(matches[0], "%Y-%m-%d %H:%M:%S")
                end_datetime   = datetime.strptime(matches[1], "%Y-%m-%d %H:%M:%S")
                current_date = start_datetime.date()
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

            # Extract the timestamp (HH:MM:SS)
            timestamp = parts[0]
            time_obj = datetime.strptime(timestamp, "%H:%M:%S").time()

            # If time resets, increment the date
            if previous_time and time_obj < previous_time:
                current_date += timedelta(days=1)

            previous_time = time_obj

            # Construct full datetime
            row_datetime = datetime.combine(current_date, time_obj)

            # Stop if beyond end time
            if row_datetime > end_datetime:
                break

            # Prepend Date and Time separately
            row = [str(current_date), timestamp] + parts[1:]
            writer.writerow(row)

print(f" Extraction complete! Data saved to {output_file}")
