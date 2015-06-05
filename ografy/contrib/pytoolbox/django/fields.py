import json

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.fields import CharField
from django.utils.encoding import smart_text
from django.utils.translation import ugettext_lazy as _


class JSONField(models.TextField, metaclass=models.SubfieldBase):
    """Simple JSON field that stores python structures as JSON strings
    on database.
    """

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('default', '{}')
        super(JSONField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        """
        Convert the input JSON value into python structures, raises
        django.core.exceptions.ValidationError if the data can't be converted.
        """
        if self.blank and not value:
            return {}
        value = value or '{}'
        if isinstance(value, bytes):
            value = str(value, 'utf-8')
        if isinstance(value, str):
            try:
                # with django 1.6 i have '"{}"' as default value here
                if value[0] == value[-1] == '"':
                    value = value[1:-1]

                return json.loads(value)
            except Exception as err:
                raise ValidationError(str(err))
        else:
            return value

    def validate(self, value, model_instance):
        """Check value is a valid JSON string, raise ValidationError on
        error."""
        if isinstance(value, str):
            super(JSONField, self).validate(value, model_instance)
            try:
                json.loads(value)
            except Exception as err:
                raise ValidationError(str(err))

    def get_prep_value(self, value):
        """Convert value to JSON string before save"""
        try:
            return json.dumps(value)
        except Exception as err:
            raise ValidationError(str(err))

    def value_to_string(self, obj):
        """Return value from object converted to string properly"""
        return smart_text(self.get_prep_value(self._get_val_from_obj(obj)))

    def value_from_object(self, obj):
        """Return value dumped to string."""
        return self.get_prep_value(self._get_val_from_obj(obj))


class NullCharField(CharField):
    """
    Character field that obeys uniqueness and nullability enforced in the database
    """
    description = _('Nullable string (up to %(max_length)s)')

    def __init__(self, *args, **kwargs):
        kwargs['null'] = True
        kwargs['blank'] = True

        super(NullCharField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if not value:
            return ''

        if isinstance(value, CharField):
            return value

        return smart_text(value)

    def get_prep_value(self, value):
        if not value:
            return None

        if isinstance(value, CharField):
            return value

        return smart_text(value)
