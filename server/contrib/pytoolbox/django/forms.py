from django.core.exceptions import ValidationError
from django.forms.fields import FileField
from django.forms.utils import ErrorDict


class AllowEmptyMixin(object):
    def full_clean(self):
        self._errors = ErrorDict()

        if not self.is_bound:
            return

        self.cleaned_data = {}

        self._clean_fields()
        self._clean_form()
        self._post_clean()

    def _clean_fields(self):
        for name, field in self.fields.items():
            value = field.widget.value_from_datadict(self.data, self.files, self.add_prefix(name))

            if not value and name not in self.data and self.empty_permitted:
                continue

            try:
                if isinstance(field, FileField):
                    initial = self.initial.get(name, field.initial)
                    value = field.clean(value, initial)
                else:
                    value = field.clean(value)

                self.cleaned_data[name] = value

                if hasattr(self, 'clean_%s' % name):
                    value = getattr(self, 'clean_%s' % name)()
                    self.cleaned_data[name] = value
            except ValidationError as e:
                self.add_error(name, e)
