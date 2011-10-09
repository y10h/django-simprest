import time
import hashlib
import os

from django.conf import settings
from django.db import models
from django.core.files import storage


class PreserveFileNameStorage(storage.FileSystemStorage):

    def get_available_name(self, name):
        unique_name = '%s:%s:%s' % (settings.SECRET_KEY, time.time(), name)
        hsh = hashlib.sha1(unique_name).hexdigest()
        prefix = hsh[:2]

        dir_name, file_name = os.path.split(name)

        return os.path.join(dir_name, prefix, hsh, file_name)

fs = PreserveFileNameStorage()

class File(models.Model):
    title = models.CharField(max_length=120)
    content = models.FileField(storage=fs, upload_to='store')
