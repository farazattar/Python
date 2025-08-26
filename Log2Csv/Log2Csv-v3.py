import re
import csv
from datetime import datetime, timedelta

input_file = "Test.txt"
output_file = "output.csv"

# Regex to match lines starting with hh:mm:ss
time_pattern = re.compile(r"^\d{2}:\d{2}:\d{2}")

# Initial date extracted from the log header (line 7)
current_date = datetime.strptime("2024-09-17", "%Y-%m-%d").date()

previous_time = None

with open(input_file, "r", encoding="utf-8", errors="ignore") as f_in, \
     open(output_file, "w", newline="", encoding="utf-8") as f_out:
    
    writer = csv.writer(f_out)

    for line in f_in:
        line = line.strip()
        if time_pattern.match(line):
            parts = re.split(r"\s+", line)

            # Extract the timestamp part
            timestamp = parts[0]
            time_obj = datetime.strptime(timestamp, "%H:%M:%S").time()

            # If time resets to 00:00:00, increment the date
            if previous_time and time_obj < previous_time:
                current_date += timedelta(days=1)

            previous_time = time_obj

            # Prepend the date string
            row = [str(current_date), timestamp] + parts[1:]
            writer.writerow(row)

print(f" Extraction complete! Data with dates saved to {output_file}")
