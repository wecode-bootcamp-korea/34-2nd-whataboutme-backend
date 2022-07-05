from django.db import models
<<<<<<< HEAD
from django.utils import timezone

from datetime import timedelta

class TimestampZone(models.Model):
     created_at = models.DateTimeField(auto_now_add=True)
     updated_at = models.DateTimeField(auto_now=True)

     class Meta:
         abstract = True

def tomorrow():
     return timezone.localtime() + timedelta(days=1)
=======

# Create your models here.
>>>>>>> 66e5923 (ADD : Database made)
