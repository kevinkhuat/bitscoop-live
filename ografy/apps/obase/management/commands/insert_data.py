import os
from django.core.management.base import BaseCommand, CommandError

from ografy.util.mongo_fixtures import load_fixture

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
MONGO_DIR = os.path.join(CURRENT_DIR, '../../fixtures_mongo')

DEMO_FILE_NAME = 'demoData.json'


class Command(BaseCommand):
    def handle(self, *args, **options):

        file_path = os.path.abspath(MONGO_DIR + '/' + DEMO_FILE_NAME)
        load_fixture(file_path)
