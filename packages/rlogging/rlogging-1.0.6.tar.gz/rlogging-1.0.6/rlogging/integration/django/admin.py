from django.contrib import admin

from rlogging.integration.django.models import RLogRecord

admin.site.register(RLogRecord)
