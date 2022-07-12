# 코드 위치 변경
from django.db import models
from django.utils import timezone

from datetime import timedelta

class TimestampZone(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

def tomorrow():
    return timezone.localtime() + timedelta(days=1)