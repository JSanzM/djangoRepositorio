from django.urls import path

from . import views

app_name = 'cds'
urlpatterns = [
    path('',views.cds_listar,name='cds'),
    path('cds/',views.cds_listar,name='cds2'),
    path('alta_cd/',views.cds_alta_cd,name='alta_cd'),
    path('buscar_cd/',views.cds_buscar_cd,name='buscar_cd'),
    path('importar_cds/',views.cds_importar_cds,name='importar_cds'),
    path('exportar_cds/',views.cds_exportar_cds,name='exportar_cds'),
    path('exportar_cds_xlsx/',views.cds_exportar_cds_xlsx,name='exportar_cds_xlsx'),
    path('editar_cd/<int:id>/', views.cds_editar_cd, name='cds_editar_cd'),
    path('borrar_cd/<int:id>/', views.cds_borrar_cd, name='cds_borrar_cd'),
]