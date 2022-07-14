from django.db import models

class Motel(models.Model):
    name      = models.CharField(max_length=50, unique=True)
    address   = models.CharField(max_length=200)
    latitude  = models.DecimalField(max_digits = 20, decimal_places = 16)
    longitude = models.DecimalField(max_digits = 20, decimal_places = 16)
    info      = models.TextField

    class Meta:
        db_table = 'motels'

class Room(models.Model):
    name           = models.CharField(max_length=100)
    motel          = models.ForeignKey(Motel, on_delete=models.CASCADE, related_name="rooms")
    original_price = models.DecimalField(max_digits = 10, decimal_places = 2, null=True)
    discount_price = models.DecimalField(max_digits = 10, decimal_places = 2, null=True)

    class Meta:
        db_table = 'rooms'

class MotelImage(models.Model):
    motel     = models.ForeignKey(Motel, on_delete=models.CASCADE, related_name="motelimages")
    image_url = models.URLField(null=True)

    class Meta:
        db_table = 'motel_images'

class RoomImage(models.Model):
    room      = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="roomimages")
    image_url = models.URLField(null=True)

    class Meta:
        db_table = 'room_images'

class Theme(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        db_table = 'themes'

class RoomTheme(models.Model):
    room  = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="roomthemes")
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE, related_name="themerooms")

    class Meta:
        db_table = 'room_themes'