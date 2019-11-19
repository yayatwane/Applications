from django.db import models


class document (models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=20)
    url = models.CharField(max_length=2048, blank='true')
    file = models.FileField(null='true', blank='true')
    signature = models.CharField(max_length=1024, blank='true')

# Create your models here.
