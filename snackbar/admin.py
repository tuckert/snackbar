from django.contrib import admin
from snackbar.models import SnackBar


class SnackBarAdmin(admin.ModelAdmin):
    pass


admin.site.register(SnackBar, SnackBarAdmin)
