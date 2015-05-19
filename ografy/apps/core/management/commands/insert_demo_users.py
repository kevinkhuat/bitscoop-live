import datetime
import os

from django.core.management.base import BaseCommand

from ografy.apps.core.models import User
from ografy.settings import EXTRA_FIXTURES


MONGO_DIR = os.path.join(EXTRA_FIXTURES, 'mongo')

DEMO_FILE_NAME = 'demoUsers.json'

def create_demo_user():
    return User(
        id=999999999,
        email='steve.howe@ografy.io',
        handle='SteveHowe',
        first_name='Steve',
        last_name='Howe',
        date_joined=datetime.datetime.now(),
        is_staff=False,
        is_active=True,
        is_verified=True,
        password_date=datetime.datetime.now(),
        last_login=datetime.datetime.now()
    )


def load_fixture(path):
    fixture_user = create_demo_user()

    fixture_user.set_password('H83mHH28R1')
    fixture_user.save()


class Command(BaseCommand):
    def handle(self, *args, **options):

        file_path = os.path.abspath(MONGO_DIR + '/' + DEMO_FILE_NAME)
        load_fixture(file_path)