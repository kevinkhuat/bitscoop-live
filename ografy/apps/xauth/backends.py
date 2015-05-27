from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

class IdentifierBackend(ModelBackend):
    def authenticate(self, identifier=None, password=None, **kwargs):
        User = get_user_model()
        user = User.objects.by_identifier(identifier).first()

        if user is not None and user.check_password(password):
            return user
