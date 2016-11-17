"""Admin classes for the drf_auth app."""
from django.contrib import admin

from . import models


class FacebookAdmin(admin.ModelAdmin):
    list_display = ['user', 'email', 'facebook_user_id', ]
    search_fields = ['user__email', 'facebook_user_id', ]
    raw_id_fields = ['user', ]

    def email(self, obj):
        return obj.user.email


admin.site.register(models.Facebook, FacebookAdmin)
