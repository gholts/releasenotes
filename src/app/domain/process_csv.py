"""
process_csv
"""
import csv
import logging
import json

from app.domain.keys import JIRA_TABLE_KEYS

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

    logging.info(json.dumps(lines))

    return lines


def verify_csv_dict_has_headers(csv_dict):
    """
    Takes in a list of dictionaries, probably one made in parse_csv and returns
    True if they contain keys, False if not.
    """
    if not csv_dict or not isinstance(csv_dict, list):
        raise ValueError("csv_dict must be provided and must be a list")

    for key in csv_dict[0].keys():
        if key in JIRA_TABLE_KEYS.ALL:
            return True

    # Kind of sneaky... if we get here, it means the list has the wrong header row
    message = "Table of issues did not have the correct headers... looking for a few in {0}".format(JIRA_TABLE_KEYS.ALL)
    import logging
    logging.error(message)
    raise ValueError(message)


