from django.contrib import admin

from .models import Tipo, Subtipo, LibroInformatica

# Register your models here.
admin.site.register(Tipo)
admin.site.register(Subtipo)

@admin.register(LibroInformatica)
class LibroInformaticaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'editorial', 'tipo', 'subtipo', 'leido')
    list_filter = ('titulo', 'autor', 'tipo__tipo', 'subtipo__subtipo', 'leido')
    search_fields = ('titulo', 'autor','tipo__descripcion', 'subtipo__descripcion','leido')