from django.db import models

from core.models import TimestampZone

class User(TimestampZone):
    kakao_id = models.BigIntegerField(unique=True)
    name     = models.CharField(max_length=20)
    nickname = models.CharField(max_length=20)
    email    = models.EmailField(null=True)

    class Meta:
        db_table = 'users'