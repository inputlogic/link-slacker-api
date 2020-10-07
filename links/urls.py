from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

from .views import (
    MessagesEventAPIView,
    StartEventAPIView,
    StopEventAPIView,
    URLListAPIView,
)

admin.autodiscover()

urlpatterns = [
    # Admin
    url(r'^admin/', admin.site.urls),
    url(r'^events/messages/', MessagesEventAPIView.as_view()),
    url(r'^events/start/', StartEventAPIView.as_view()),
    url(r'^events/stop/', StopEventAPIView.as_view()),
    url(r'^events/', URLListAPIView.as_view()),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.ENV == settings.DEV:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)