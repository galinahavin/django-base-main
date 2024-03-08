from django.db import models
from django.contrib.auth.models import User


class Event(models.Model):
    date = models.DateField()
    name = models.CharField(max_length=100)
    description = models.TextField()
    tags = models.CharField(
        max_length=100, default=None, null=True, blank=True)
    link = models.URLField()
    revisions_count = models.IntegerField(default=1)

    class Meta:
        ordering = ('date',)

def tags_list(self):
    return self.tags.split(',')


class WikiRevisionEvent(models.Model):
    event_date = models.DateField()
    page_title = models.CharField(max_length=100)
    page_description = models.TextField()
    event_tags = models.CharField(
        max_length=100, default=None, null=True, blank=True)
    page_url = models.URLField()
    revisions_count = models.IntegerField(default=1)
    class Meta:
        ordering = ('event_date',)
