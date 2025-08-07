from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from django.contrib.auth.models import Group

from django.contrib import admin

admin.site.unregister(Group)
