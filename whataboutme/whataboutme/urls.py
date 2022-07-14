from django.urls import path, include

urlpatterns = [
    path('v1/api/users', include('users.urls')),
]