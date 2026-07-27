from django.urls import path

from . import views

app_name = 'libro_trenes'
urlpatterns = [
    path('',views.libro_trenes_listar,name='libro_trenes'),
    path('libro_trenes/',views.libro_trenes_listar,name='libro_trenes2'),
    path('alta_libro_trenes/',views.libro_trenes_alta_libro,name='libro_trenes_alta'),
    path('buscar_libro_trenes/',views.libro_trenes_buscar_libro,name='libro_trenes_buscar'),
    path('importar_libro_trenes/',views.libro_trenes_importar_libro,name='libro_trenes_importar'),
    path('exportar_libro_trenes/',views.libro_trenes_exportar_libro,name='libro_trenes_exportar'),
    path('exportar_libro_trenes_xlsx/',views.libro_trenes_exportar_libro_xlsx,name='libro_trenes_exportar_xlsx'),
    path('editar_libro_trenes/<int:id>/', views.libro_trenes_editar_libro, name='libro_trenes_editar_libro'),
    path('borrar_libro_trenes/<int:id>/', views.libro_trenes_borrar_libro, name='libro_trenes_borrar_libro'),
    ]