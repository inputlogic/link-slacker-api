from django.contrib import admin
from django.conf.locale.es import formats as es_formats
from django.contrib.admin import DateFieldListFilter
from django.utils.html import format_html

from .models import URL

es_formats.DATETIME_FORMAT = "d M Y H:i:s"


@admin.register(URL)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("title", "show_link_url", "description", "created_on")

    list_filter = (
        ('created_on', DateFieldListFilter),
    )

    def show_link_url(self, obj):
        return format_html("<a href='{url}'>{url}</a>", url=obj.link)
