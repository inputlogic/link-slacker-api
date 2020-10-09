from django.db import models


class Team(models.Model):
    team_id = models.CharField(max_length=9, default="T02FBR21U")
    team_domain = models.CharField(max_length=100, default="inputlogic")


class Channel(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    channel_id = models.CharField(max_length=100, default="")
    channel_name = models.CharField(max_length=100, default="")
    channel_text = models.CharField(max_length=100, default="")
    listen = models.BooleanField()

    class Meta:
        ordering = ("channel_name", "channel_id")


class URL(models.Model):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
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

