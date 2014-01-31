""" Tests for app.models.unique. """

# google imports
from test.fixtures.appengine import GaeTestCase
from unique import build_unique_value, set_unique, clear_unique, UniqueConstraintViolatedException

class UniqueTests(GaeTestCase):
    """ Tests for _Unique class. """

    def setUp(self):
        """
        Prepare the test environment before a test run
        """
        super(UniqueTests, self).setUp()

    def test_build_unique_value_requires_constraint_name(self):
        """
        ensures build_unique_value requires constraint name
        """
        self.assertRaises(ValueError, build_unique_value, None, 'value')
        self.assertRaises(ValueError, build_unique_value, '', 'value')
        
    def test_build_unique_value_requires_at_least_one_value(self):
        """
        ensures build_unique_value_requires_at_least_one_value
        """
        self.assertRaises(ValueError, build_unique_value, 'constraint_name')
        
    def test_constraint_name_in_key_name(self):
        """
        ensures constraint_name_in_key_name
        """
        constraint_name = 'c_name'
        key_name = build_unique_value(constraint_name, 'value')
        self.assertTrue(constraint_name in key_name)
        
    def test_all_values_in_key_name(self):
        """
        ensures all_values_in_key_name
        """
        value1 = 'foo'
        value2 = 'bar'
        key_name = build_unique_value('c_name', value1, value2)
        self.assertTrue(value1 in key_name)
        self.assertTrue(value2 in key_name)
        
class SetUniqueConstraint(GaeTestCase):
    """ Tests for set_unique. """

    def setUp(self):
        """
        Prepare the test environment before a test run
        """
        super(SetUniqueConstraint, self).setUp()

    def tearDown(self):
        """
        Restore the environment following a test run
        """
        self.testbed.deactivate()
    
    def test_constraint_name_required(self):
        """
        ensures constraint_name_required
        """
        self.assertRaises(ValueError, set_unique, None, 'value')
        self.assertRaises(ValueError, set_unique, '', 'value')
        
    def test_at_least_one_value_required(self):
        """
        ensures at_least_one_value_required
        """
        self.assertRaises(ValueError, set_unique, 'constraint_name')
        
    def test_multiple_sets_raises_exception(self):
        """
        ensures multiple_sets_raises_exception
        """
        constraint_name = 'c_name'
        value = 'value'
        set_unique(constraint_name, value)
        self.assertRaises(UniqueConstraintViolatedException, set_unique, constraint_name, value)

class ClearUniqueConstraint(GaeTestCase):
    """ Tests for clear_unique. """

    def setUp(self):
        """
        Prepare the test environment before a test run
        """
        super(ClearUniqueConstraint, self).setUp()

    def tearDown(self):
        """
        Restore the environment following a test run
        """
        self.testbed.deactivate()

    def test_constraint_name_required(self):
        """
        ensures constraint_name_required
        """
        self.assertRaises(ValueError, clear_unique, None, 'value')
        self.assertRaises(ValueError, clear_unique, '', 'value')

    def test_at_least_one_value_required(self):
        """
        ensures at_least_one_value_required
        """
        self.assertRaises(ValueError, clear_unique, 'constraint_name')
        
    def test_unknown_constraint_does_not_raise_exception(self):
        """
        ensures unknown_constraint_does_not_raise_exception
        """
        try:
            clear_unique('never-heard', 'of-you')
        except Exception:
            self.fail('Previous line should not raise.')

    def test_constraint_can_be_reused(self):
        """
        ensures constraint_can_be_reused
        """
        constraint_name = 'c_name'
        value1 = 'value1'
        value2 = 'value2'
        set_unique(constraint_name, value1, value2)
        clear_unique(constraint_name, value1, value2)
        try:
            set_unique(constraint_name, value1, value2)
        except Exception:
            self.fail('Previous line should not raise.')