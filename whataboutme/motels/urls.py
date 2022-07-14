from django.urls import path
from motels.views import MotelListQuery, RoomListView

urlpatterns = [
    path('/list', MotelListQuery.as_view()),
    path('/rooms', RoomListView.as_view())
]