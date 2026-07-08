from django.urls import path

from . import views

app_name = 'libro_electronico'
urlpatterns = [
    path('',views.libro_electronico_listar,name='libro_electronico'),
    path('libro_electronico/',views.libro_electronico_listar,name='libro_electronico2'),
    path('alta_libro_electronico/',views.libro_electronico_alta_libro,name='libro_electronico_alta'),
    path('buscar_libro_electronico/',views.libro_electronico_buscar_libro,name='libro_electronico_buscar'),
    path('importar_libro_electronico/',views.libro_electronico_importar_libro,name='libro_electronico_importar'),
    path('exportar_libro_electronico/',views.libro_electronico_exportar_libro,name='libro_electronico_exportar'),
    path('exportar_libro_electronico_xlsx/',views.libro_electronico_exportar_libro_xlsx,name='libro_electronico_exportar_xlsx'),
    path('editar_libro_electronico/<int:id>/', views.libro_electronico_editar_libro, name='libro_electronico_editar_libro'),
    path('borrar_libro_electronico/<int:id>/', views.libro_electronico_borrar_libro, name='libro_electronico_borrar_libro'),
]