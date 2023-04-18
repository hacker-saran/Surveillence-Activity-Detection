from unicodedata import name
from django.db import models

class first(models.Model):
    name:models.CharField(max_length=100)
