from django.urls import path

from . import views

app_name = 'juegos'
urlpatterns = [
    path('',views.juegos_listar,name='juegos'),
    path('juegos/',views.juegos_listar,name='juegos2'),
    path('alta_juego/',views.juegos_alta_juego,name='alta_juego'),
    path('buscar_juego/',views.juegos_buscar_juego,name='buscar_juego'),
    path('importar_juegos/',views.juegos_importar_juegos,name='importar_juegos'),
    path('exportar_juegos/',views.juegos_exportar_juegos,name='exportar_juegos'),
    path('exportar_juegos_xlsx/',views.juegos_exportar_juegos_xlsx,name='exportar_juegos_xlsx'),
    path('editar_juego/<int:id>/', views.juegos_editar_juego, name='juegos_editar_juego'),
    path('borrar_juego/<int:id>/', views.juegos_borrar_juego, name='juegos_borrar_juego'),
]