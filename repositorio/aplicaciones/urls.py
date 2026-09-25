from django.urls import path

from . import views

app_name = 'aplicaciones'
urlpatterns = [
    path('',views.aplicaciones_listar,name='aplicaciones'),
    path('aplicaciones/',views.aplicaciones_listar,name='aplicaciones2'),
    path('alta_aplicacion/',views.aplicaciones_alta_aplicacion,name='alta_aplicacion'),
    path('buscar_aplicacion/',views.aplicaciones_buscar_aplicacion,name='buscar_aplicacion'),
    path('importar_aplicaciones/',views.aplicaciones_importar_aplicaciones,name='importar_aplicaciones'),
    path('exportar_aplicaciones/',views.aplicaciones_exportar_aplicaciones,name='exportar_aplicaciones'),
    path('exportar_aplicaciones_xlsx/',views.aplicaciones_exportar_aplicaciones_xlsx,name='exportar_aplicaciones_xlsx'),
    path('editar_aplicacion/<int:id>/', views.aplicaciones_editar_aplicacion, name='aplicaciones_editar_aplicacion'),
    path('borrar_aplicacion/<int:id>/', views.aplicaciones_borrar_aplicacion, name='aplicaciones_borrar_aplicacion'),
]