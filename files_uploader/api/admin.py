"""Модуль для отображения модели в админ-панели."""

from api.models import File
from django.contrib import admin


class FileAdmin(admin.ModelAdmin):
    """Отображение модели в админ-панели."""

    list_display = ('pk', 'file', 'uploaded_at', 'processed')


admin.site.register(File, FileAdmin)
