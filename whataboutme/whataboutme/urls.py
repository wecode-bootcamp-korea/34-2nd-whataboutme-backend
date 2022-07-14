from django.urls import path, include

urlpatterns = [
    path('v1/api/users', include('users.urls')),
    path('v1/api/motels', include('motels.urls')),
    path('v1/api/reservation', include('reservations.urls'))
]