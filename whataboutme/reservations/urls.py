from django.urls import path

from reservations.views import MakeReservationView

urlpatterns = [
    path('', MakeReservationView.as_view())
]