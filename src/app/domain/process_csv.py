"""
process_csv
"""
import csv

def parse_csv(csv_string):
    """
    Takes in a string that is a csv, with lines separated with \r\n
    """
    reader = csv.DictReader(csv_string.split('\r\n'), dialect="excel", delimiter="\t")
    lines = []
    for line in reader:
        lines.append(line)

    return lines