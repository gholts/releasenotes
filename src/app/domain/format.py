"""
format
"""
from keys import JIRA_TABLE_KEYS


def format_email_text(issue_list, products):
    """
    Takes a list of issues and returns the full email required for a release
    """
    # Set up the tldr dictionaries
    tldr = {product:[] for product in products}

    email_html = ""

    issue_string = "<a href='http://vendasta.jira.com/browse/{0}'>{0}</a> " \
                   " {1} - {2} - {3}<br>"

    for issue in issue_list:
        key = issue.get(JIRA_TABLE_KEYS.KEY)
        summary = issue.get(JIRA_TABLE_KEYS.SUMMARY)
        issue_type = issue.get(JIRA_TABLE_KEYS.ISSUE_TYPE)
        status = issue.get(JIRA_TABLE_KEYS.STATUS)

        # Get the project
        project = key.split("-")[0]
        tldr[project].append(summary)

        formatted_string = issue_string.format(key, summary, issue_type, status)
        email_html += formatted_string

    tldr_html = "<strong>TL;DR</strong>:<br>"

    for project in tldr.keys():
        tldr_html += "{0}:<br>".format(project)
        for item in tldr[project]:
            tldr_html += "- {0}<br>".format(item)

    return tldr_html + "<br>" + email_html
