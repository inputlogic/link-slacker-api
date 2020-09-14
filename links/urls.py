from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from .views import (
    MessagesEventAPIView,
    StartEventAPIView,
    StopEventAPIView,
    URLListAPIView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    url(r"^events/messages/", MessagesEventAPIView.as_view()),
    url(r"^events/start/", StartEventAPIView.as_view()),
    url(r"^events/stop/", StopEventAPIView.as_view()),
    url(r"^events/", URLListAPIView.as_view()),
]
