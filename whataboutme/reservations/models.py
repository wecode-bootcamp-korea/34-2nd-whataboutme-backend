from django.db import models
from django.utils import timezone

from core.utils import TimestampZone, tomorrow

from user.models import User
from motel.models import Room

class Reservation(TimestampZone):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="reservationrooms")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reservationusers")
    name = models.CharField(max_length=50)
    checkin = models.DateField(default = timezone.localtime())
    checkout = models.DateField(default = tomorrow)
    price = models.DecimalField(max_digits = 10, decimal_places = 2)

    class Meta:
        db_table = 'reservations'