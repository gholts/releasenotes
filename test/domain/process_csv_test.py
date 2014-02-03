"""
Tests for processing CSV files
"""
from app.domain.process_csv import parse_csv

from test.fixtures.appengine import GaeTestCase

class CsvParseTests(GaeTestCase):
    def test_csv_string_required(self):
        self.assertRaises(ValueError, parse_csv, None)