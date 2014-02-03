"""
process_csv
"""
import csv

def parse_csv(csv_string, line_terminator="\r\n", dialect="excel", delimiter="\t"):
    """
    Takes in a string that is a csv, with lines separated with \r\n
    """
    if not csv_string:
        raise ValueError("CSV string must not be empty")
    reader = csv.DictReader(csv_string.split(line_terminator), dialect=dialect, delimiter=delimiter)
    lines = []
    for line in reader:
        lines.append(line)

    return lines