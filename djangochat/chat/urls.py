from django.urls import path
from .views import health_check
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("checkview", views.checkview, name="checkview"),
    path("getMessages/<str:room>/", views.getMessages, name="getMessages"),
    path("send", views.send, name="send"),
    path("health/", health_check, name="health"),   # moved above <str:room>/
    path("<str:room>/", views.room, name="room"),
]