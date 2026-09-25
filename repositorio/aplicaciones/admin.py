from django.contrib import admin

from .models import Origen, Aplicaciones

# Register your models here.
admin.site.register(Origen)

@admin.register(Aplicaciones)
class AplicacionesAdmin(admin.ModelAdmin):
    list_display = ('aplicacion', 'origen', 'instalar', 'favoritos', 'notas')
    list_filter = ('aplicacion', 'origen__origen', 'instalar', 'favoritos')
    search_fields = ('aplicacion', 'origen__origen', 'instalar', 'favoritos')