#customestorage
import os 
from django.conf import settings
from django.core.files.storage import FileSystemStorage
#from settings import RUTA_PROYECTO


from django.db.models import FileField
from django.forms import forms

class CustomCheckFileField(FileField):
    def __init__(self, custom_check=None, error_message=None, **kwargs):

        self.error_message=error_message

        if callable(custom_check):
            self.custom_check = custom_check

        super(CustomCheckFileField, self).__init__(**kwargs)

    def clean(self, *args, **kwargs):
        data = super(CustomCheckFileField, self).clean(*args, **kwargs)

        file = data.file

        #args[1] is the model instance
        if not self.custom_check(args[1], self.generate_filename(args[1], file.name)):
            raise forms.ValidationError(self.error_message)
        return data

    def custom_check(self, filename):
        return True



#custom FileSystemStorage which return same name for existing file (also deletes existing files on save
#some_other.py
from django.core.files.storage import FileSystemStorage

class OverwriteStorage(FileSystemStorage):

    def _save(self, name, content):
        if self.exists(name):
            self.delete(name)
        return super(OverwriteStorage, self)._save(name, content)

    def get_available_name(self, name):
        return name




 
