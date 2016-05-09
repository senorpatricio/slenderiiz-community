from __future__ import unicode_literals

from django_resized import ResizedImageField
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone
# from django.utils.text import slugify


def upload_location(instance, filename):
    return "%s/%s" % (instance.id, filename)


class PostManager(models.Manager):
    def active(self, *args, **kwargs):
        return super(PostManager, self).filter(draft=True).filter(publish__lte=timezone.now())


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    pounds_lost = models.IntegerField(default=0)
    beforeimage = ResizedImageField(size=[100, 200], crop=['middle', 'center'])
    afterimage = ResizedImageField(size=[100, 200], crop=['middle', 'center'])
    draft = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.first_name

    def get_absolute_url(self):  # instance method
        return reverse("posts:detail", kwargs={"id": self.id})  # most dynamic way to do it

    class Meta:
        ordering = ["-id", "-timestamp"]
