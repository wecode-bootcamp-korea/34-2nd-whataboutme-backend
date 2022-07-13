from django.urls import path
from reservations.views import MakeReservationView

urlpatterns = [
    path('/make', MakeReservationView.as_view())
]