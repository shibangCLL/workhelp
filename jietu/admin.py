from django.contrib import admin

# Register your models here.
from .models import DoaminType, Doamin, Jietu,DoaminExpirationDate

from import_export.admin import ImportExportModelAdmin
from .resource import DoaminResource


@admin.register(Doamin)
class DoaminAdmin(ImportExportModelAdmin):
    resource_class = DoaminResource


admin.site.register(DoaminType)
admin.site.register(Jietu)
admin.site.register(DoaminExpirationDate)
