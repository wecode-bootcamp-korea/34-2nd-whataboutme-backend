from django.urls import path, include

urlpatterns = [
    path('v1/api', include('motel.urls'))
]
