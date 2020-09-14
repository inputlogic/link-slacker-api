from django.db import models


class URL(models.Model):
    title = models.CharField(max_length=100, null=True)
    link = models.CharField(max_length=100)
    description = models.TextField(max_length=1000, null=True)
    image = models.TextField(max_length=1000, null=True)
    msg = models.CharField(max_length=100, default="")
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("title", "link")

    def __str__(self):
        return self.link


class Channel(models.Model):
    channel_id = models.CharField(max_length=100)
    listen = models.BooleanField()
