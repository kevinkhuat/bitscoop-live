import os

from django.core.files.storage import FileSystemStorage


class OverwriteFileSystemStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        path = os.path.abspath(os.path.join(self.location, name))

        if self.exists(name):
            os.remove(path)

        return name
