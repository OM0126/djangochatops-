from django.urls import path,re_path
from .views import health_check
from . import views

urlpatterns = [
    re_path(r"^favicon\.ico/?$", views.favicon, name="favicon"),
    path("", views.home, name="home"),
    path("checkview", views.checkview, name="checkview"),
    path("getMessages/<str:room>/", views.getMessages, name="getMessages"),
    path("send", views.send, name="send"),
    path("health/", health_check, name="health"), 
    path("<str:room>/", views.room, name="room"),
]