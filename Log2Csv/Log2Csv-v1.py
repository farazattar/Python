import re
import csv

# Input and output file names
input_file = "Test.txt"
output_file = "output.csv"

# Regex to match lines starting with hh:mm:ss
time_pattern = re.compile(r"^\d{2}:\d{2}:\d{2}")

with open(input_file, "r", encoding="utf-8", errors="ignore") as f_in, \
     open(output_file, "w", newline="", encoding="utf-8") as f_out:
    
    writer = csv.writer(f_out)

    for line in f_in:
        line = line.strip()
        if time_pattern.match(line):
            # Split on whitespace (multiple spaces)
            parts = re.split(r"\s+", line)
            writer.writerow(parts)

print(f" Extraction complete! Data saved to {output_file}")
