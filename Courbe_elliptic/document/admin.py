from django.contrib import admin
from .models import document


class documentAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'file')


admin.site.register(document, documentAdmin)
# Register your models here.
