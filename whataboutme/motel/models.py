from django.db import models
from django.utils import timezone

from core.utils import TimestampZone, tomorrow
from user.models import User

class Motel(models.Model):
    name = models.CharField(max_length=50, unique=True)
    address = models.CharField(max_length=200)
    latitude = models.DecimalField(max_digits = 10, decimal_places = 7)
    longitude = models.DecimalField(max_digits = 10, decimal_places = 7)
    info = models.TextField

    class Meta:
        db_table = 'motels'

class Room(models.Model):
    name = models.CharField(max_length=100)
    motel = models.ForeignKey(Motel, on_delete=models.CASCADE, related_name="motel")
    original_price = models.DecimalField(max_digits = 10, decimal_places = 2)
    discount_price = models.DecimalField(max_digits = 10, decimal_places = 2)

    class Meta:
        db_table = 'rooms'

class MotelImage(models.Model):
    motel = models.ForeignKey(Motel, on_delete=models.CASCADE, related_name="motelimage")
    image_url = models.URLField(null=True)

    class Meta:
        db_table = 'motel_images'

class RoomImage(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="roomimages")
    image_url = models.URLField(null=True)

    class Meta:
        db_table = 'room_images'


class Reservation(TimestampZone):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="room")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    name = models.CharField(max_length=50)
    checkin = models.DateField(default = timezone.localtime())
    checkout = models.DateField(default = tomorrow)
    price = models.DecimalField(max_digits = 10, decimal_places = 2)

    class Meta:
        db_table = 'reservations'

class Theme(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        db_table = 'themes'

class RoomTheme(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="room_theme")
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE, related_name="theme_room")

    class Meta:
        db_table = 'room_themes'

