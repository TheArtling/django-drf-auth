"""Models for the drf_auth app."""
from django.db import models


class Facebook(models.Model):
    user = models.ForeignKey('auth.User')
    facebook_user_id = models.CharField(max_length=1024)
