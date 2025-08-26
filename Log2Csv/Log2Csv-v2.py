import re
import csv

input_file = "Test.txt"
output_file = "output.csv"

# Regex to detect lines with timestamps
time_pattern = re.compile(r"^\d{2}:\d{2}:\d{2}")

headers = []
data_started = False
data_rows = []

with open(input_file, "r", encoding="utf-8", errors="ignore") as f_in:
    for line in f_in:
        line = line.rstrip()

        # Collect headers (the two lines just above the dashed line)
        if "GENERATOR" in line and "GT POWER" in line:
            headers = re.split(r"\s{2,}", line.strip())
        elif line.strip().startswith("-"):
            continue  # skip dashed line
        elif time_pattern.match(line):
            data_started = True
            parts = re.split(r"\s+", line.strip())
            data_rows.append(parts)

# Insert "Time" column at the beginning of headers
if headers:
    headers = ["Time"] + headers

# Write CSV
with open(output_file, "w", newline="", encoding="utf-8") as f_out:
    writer = csv.writer(f_out)
    if headers:
        writer.writerow(headers)
    writer.writerows(data_rows)

print(f" Extraction complete! Data with headers saved to {output_file}")
