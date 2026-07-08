from django.urls import path

from . import views

app_name = 'libro_informatica'
urlpatterns = [
    path('',views.libro_informatica_listar,name='inicial'),
    path('libro_informatica/',views.libro_informatica_listar,name='libro_informatica'),
    path('alta_libro/',views.libro_informatica_alta_libro,name='alta_libro_informatica'),
    path('buscar_libro/',views.libro_informatica_buscar_libro,name='buscar_libro_informatica'),
    path('importar_libro/',views.libro_informatica_importar_libro,name='importar_libro_informatica'),
    path('exportar_libro/',views.libro_informatica_exportar_libro,name='exportar_libro_informatica'),
    path('exportar_libro_xlsx/',views.libro_informatica_exportar_libro_xlsx,name='exportar_libro_informatica_xlsx'),
    path('editar_libro/<int:id>/', views.libro_informatica_editar_libro, name='libro_informatica_editar_libro'),
    path('borrar_libro/<int:id>/', views.libro_informatica_borrar_libro, name='libro_informatica_borrar_libro'),
]