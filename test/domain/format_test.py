"""
Tests for formatting text
"""

from app.domain.format import format_email_text

from test.fixtures.appengine import GaeTestCase

class FormatTests(GaeTestCase):
    def test_issue_list_is_required(self):
        self.assertRaises(ValueError, format_email_text, None, "MS")

    def test_projects_is_required(self):
        self.assertRaises(ValueError, format_email_text, "Blah", None)