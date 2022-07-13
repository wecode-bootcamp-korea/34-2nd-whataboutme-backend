from django.urls import path, include

urlpatterns = [
    path('v1/api/user', include('user.urls')),
    path('v1/api/motel', include('motel.urls')),
    path('v1/api/reservation', include('reservations.urls'))
]
