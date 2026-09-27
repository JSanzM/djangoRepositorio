from django.contrib import admin

from .models import Juegos, TipoJuego

# Register your models here.
admin.site.register(TipoJuego)

@admin.register(Juegos)
class JuegosAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipoJuego', 'instalar', 'origen', 'notas')
    list_filter = ('nombre', 'tipoJuego__tipoJuego', 'instalar', 'origen__origen', 'notas')
    search_fields = ('nombre', 'tipoJuego__tipoJuego','origen__origen','instalar')