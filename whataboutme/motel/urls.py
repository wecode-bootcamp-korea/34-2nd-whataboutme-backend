from django.urls import path
from motel.views import MotelListQuery

urlpatterns = [
    path('/motel', MotelListQuery.as_view())
]