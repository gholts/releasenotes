"""
format
"""
from app.domain.keys import JIRA_TABLE_KEYS, FORMAT_KEYS, VANILLA_ISSUE_STRING, \
                            COLOURFUL_ISSUE_STRING, JIRA_ISSUE_TYPES


def format_email_text(issue_list, products, issue_format=FORMAT_KEYS.VANILLA):
    """
    Takes a list of issues and returns the full email required for a release
    """
    if not issue_list:
        raise ValueError("The issue list cannot be empty")
    if not products:
        raise ValueError("Products cannot be empty")

    # Set up the tldr dictionaries
    tldr = {product:[] for product in products.decode('utf-8').split(',')}

    email_html = ""

    for issue in issue_list:
        key = issue.get(JIRA_TABLE_KEYS.KEY)
        summary = issue.get(JIRA_TABLE_KEYS.SUMMARY)
        issue_type = issue.get(JIRA_TABLE_KEYS.ISSUE_TYPE)
        status = issue.get(JIRA_TABLE_KEYS.STATUS)

        # Get the project
        project = key.split("-")[0]
        # Add it to the tldr list if it's a story, only
        if issue_type == JIRA_ISSUE_TYPES.STORY:
            tldr[project].append(summary)

        if issue_format == FORMAT_KEYS.COLOURFUL:
            issue_class = issue_type.lower().split(" ")
            issue_class = "-".join(issue_class) + "-type"
            formatted_string = COLOURFUL_ISSUE_STRING.format(key, summary, issue_type, status, issue_class)
        else:
            # Must be vanilla
            formatted_string = VANILLA_ISSUE_STRING.format(key, summary, issue_type, status)

        email_html += formatted_string

    tldr_html = "<strong>TL;DR</strong>:<br>"

    for project in tldr.keys():
        tldr_html += "{0}:<br>".format(project)
        for item in tldr[project]:
            tldr_html += "- {0}<br>".format(item)

    return tldr_html + "<br>" + email_html
