from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class IdentifierBackend(ModelBackend):
    def authenticate(self, identifier=None, password=None, **kwargs):
        user_model = get_user_model()
        user = user_model.objects.by_identifier(identifier).first()

        if user is not None and user.check_password(password):
            return user
