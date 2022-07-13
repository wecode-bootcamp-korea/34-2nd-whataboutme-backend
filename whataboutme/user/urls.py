from django.urls import path
from user.views import MakeUser

urlpatterns = [
    path('/make', MakeUser.as_view())
]