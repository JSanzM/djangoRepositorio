from django.contrib import admin

from .models import LibroElectronico


# Register your models here.
@admin.register(LibroElectronico)
class LibroElectronicoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'serie', 'bajado', 'notas')
    list_filter = ('titulo', 'autor', 'serie', 'bajado', 'notas')
    search_fields = ('titulo', 'autor', 'serie', 'bajado', 'notas')