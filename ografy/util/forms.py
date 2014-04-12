from __future__ import unicode_literals

from django.core.exceptions import NON_FIELD_ERRORS, ValidationError
from django.forms import Form as BaseForm, ModelForm as BaseModelForm
import six


class FormMixin(object):
    """
    A temporary patch mixin to bring forms in line with desired Django 1.7 functionality.
    """
    def add_error(self, error, field=None):
        """
        Update the content of `self._errors`.

        The `field` argument is the name of the field to which the errors
        should be added. If its value is None the errors will be treated as
        NON_FIELD_ERRORS.

        The `error` argument can be a single error, a list of errors, or a
        dictionary that maps field names to lists of errors. What we define as
        an "error" can be either a simple string or an instance of
        ValidationError with its message attribute set and what we define as
        list or dictionary can be an actual `list` or `dict` or an instance
        of ValidationError with its `error_list` or `error_dict` attribute set.

        If `error` is a dictionary, the `field` argument *must* be None and
        errors will be added to the fields that correspond to the keys of the
        dictionary.
        """
        if isinstance(error, six.string_types):
            error = [error]

        if not isinstance(error, ValidationError):
            # Normalize to ValidationError and let its constructor
            # do the hard work of making sense of the input.
            error = ValidationError(error)

        if hasattr(error, 'error_dict'):
            if field is not None:
                raise TypeError('The argument `field` must be `None` when the `error` argument contains errors for multiple fields.')
            else:
                error = error.error_dict
        else:
            error = {
                field or NON_FIELD_ERRORS: error.error_list
            }

        for field_name, errors in six.iteritems(error):
            if field_name not in self.errors:
                if field_name != NON_FIELD_ERRORS and field_name not in self.fields:
                    raise ValueError('"%s" has no field named "%s"' % (self.__class__.__name__, field_name))

                self._errors[field_name] = self.error_class()

            self._errors[field_name].extend(errors)

            if field_name in self.cleaned_data:
                del self.cleaned_data[field_name]

    def remove_errors(self, field):
        # FIXME: Get this to actually work with the `is_invalid` method. Right now it appears to return `False` even when you remove all errors.
        self._errors[field] = self.error_class()


class Form(BaseForm, FormMixin):
    """
    A new base Form with the add_error mixin to hold over until Django 1.7.
    """


class ModelForm(BaseModelForm, FormMixin):
    """
    A new base ModelForm with the add_error mixin to hold over until Django 1.7.
    """
