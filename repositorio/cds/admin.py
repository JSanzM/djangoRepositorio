from django.contrib import admin

from .models import Grupo, Tipo, Cds

# Register your models here.
admin.site.register(Grupo)
admin.site.register(Tipo)

@admin.register(Cds)
class CdsAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'grupo', 'anyo', 'notas', 'copiado', 'falta', 'tipo')
    list_filter = ('titulo', 'grupo__grupo', 'tipo__tipo', 'falta', 'copiado')
    search_fields = ('titulo', 'grupo__grupo', 'tipo__tipo', 'falta', 'copiado')