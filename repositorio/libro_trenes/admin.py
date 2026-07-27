from django.contrib import admin

from .models import LibroTrenes


# Register your models here.
@admin.register(LibroTrenes)
class LibroTrenesAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'editorial', 'anyo', 'leido')
    list_filter = ('titulo', 'autor', 'editorial', 'anyo', 'leido')
    search_fields = ('titulo', 'autor', 'editorial', 'anyo', 'leido')