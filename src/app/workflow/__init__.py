""" This package holds functions for the view's POST actions to call to get work done.

Each view's POST should only call a single workflow function to get its work done.

Forms are stored in this package and are the method of communication between the view and this packge.
"""
import re
from keys import KEY
from wtforms.form import Form
from wtforms.fields import TextField, TextAreaField, Field
from wtforms.validators import ValidationError
from wtforms.widgets import TextInput

class CleaningForm(Form):
    """ A form that cleans it's values (strips, turns '' into None) on validate. 
    
    This form also keeps track of when validate() was called and caches the result.
    """
        
    def validate(self):
        """ Validate (and clean on success) the form. """
            
        result = super(CleaningForm, self).validate()
        
        if not result:
            return result
            
        for field in self._fields.itervalues():
            if field.__class__ is TextField or field.__class__ is TextAreaField:
                if field.data:
                    if hasattr(field.data, 'strip'):
                        field.data = field.data.strip()
                else:
                    field.data = None
                    
        return result

    def _get_translations(self):
        """
        When passing a dictionary (instead of a Request object) for the form data
        an error occurs in wtforms.form._get_translations:102 so this
        method is to override the method and avoid that error.
        """
        # TODO: remove this method and determine why it is failing in wtforms.form
        return None

class RegexpList(object):
    """
    Taken from wtforms/validators.py but adapted to handle list field data.

    Validates the field against a user provided regexp.

    :param regex:
        The regular expression string to use. Can also be a compiled regular
        expression pattern.
    :param flags:
        The regexp flags to use, for example re.IGNORECASE. Ignored if
        `regex` is not a string.
    :param message:
        Error message to raise in case of a validation error.
    """
    def __init__(self, regex, flags=0, message=None):
        if isinstance(regex, basestring):
            regex = re.compile(regex, flags)
        self.regex = regex
        self.message = message

    def __call__(self, form, field):
        for value in field.data:
            if not self.regex.match(value or u''):
                if self.message is None:
                    self.message = field.gettext(u'Invalid input.')

                raise ValidationError(self.message)

class TextListField(Field):
    """
    Field for converting comma delimited list into an actual python list.
    See here for more info on Custom Fields: http://wtforms.simplecodes.com/docs/0.6.1/fields.html#custom-fields
    """
    widget = TextInput()

    def __init__(self, *args, **kwargs):
        """ Declare self.data to quiet pylint. """
        self.data = None
        kwargs['default'] = kwargs.get('default', [])
        super(TextListField, self).__init__(*args, **kwargs)

    def _value(self):
        """ Return the value of this field as a string. """
        if self.data:
            return u', '.join(self.data)
        else:
            return u''

    def process_formdata(self, valuelist):
        """
        This will be called during form construction with data supplied through the formdata argument.
        """
        if valuelist:
            # data entered from form
            self.data = [text.strip() for text in valuelist[0].split(',') if text.strip()]
        else:
            # batch import list of fields
            self.data = []

class EmailListField(TextListField):
    """ Lowercases the provided email addresses and ensures they are valid. """

    def process_formdata(self, valuelist):
        """ Lower case the email addresses. """
        super(EmailListField, self).process_formdata(valuelist)
        self.data = [value.lower() for value in self.data if value]

    def post_validate(self, form, validation_stopped):
        """ Validate email addresses are of the correct format. """
        if validation_stopped:
            return

        email_validator = RegexpList(KEY.EMAIL_REGEX_EXPRESSION, message="Please provide a valid email address.")
        email_validator(form, self)