"""
keys
"""
VANILLA_ISSUE_STRING = "[{2}] <a href='http://vendasta.jira.com/browse/{0}'>{0}</a> " \
                         "{1} - {3}<br>"
COLOURFUL_ISSUE_STRING = "[<span class='{4}'>{2}</span>] <a href='http://vendasta.jira.com/browse/{0}'>{0}</a> " \
                         "{1} - {3}<br>"


class JIRA_TABLE_KEYS(object):
    KEY = "Key"
    SUMMARY = "Summary"
    ISSUE_TYPE = "Issue Type"
    PRIORITY = "Priority"
    STATUS = "Status"


class FORMAT_KEYS(object):
    VANILLA = "vanilla"
    COLOURFUL = "colourful"