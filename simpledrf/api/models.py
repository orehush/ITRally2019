from django.contrib.auth.models import User
from django.db import models
from django_extensions.db.models import TimeStampedModel

from api.helpers import get_sub_obj


class InheritanceMixin:
    @property
    def child(self):
        return get_sub_obj(self)


class Author(InheritanceMixin, User):
    rating = models.FloatField(default=0)


class Reviewer(InheritanceMixin, User):
    level = models.PositiveIntegerField(default=0)


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Post(TimeStampedModel):
    class Meta:
        ordering = ('-modified', )

    title = models.CharField(max_length=255)
    body = models.TextField()
    tags = models.ManyToManyField(Tag, related_name='posts')
    author = models.ForeignKey(Author, models.CASCADE, related_name='posts')
    reviewed_by = models.ManyToManyField(Reviewer)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.title
