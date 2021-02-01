"""bookeame URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from books import views
from django.conf.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
    #URLs CARGAR BD E INDEXAR
    path('carga-generos/', views.carga_generos),
    path('carga-bd/', views.carga_bd),
    path('carga-ttl/', views.carga_ttl),
    path('carga-libros/',views.carga_libros),
    path('carga-libros-leidos/',views.carga_libros_leidos),
    path('cargaldts/', views.carga_libros_dataset),
    path('indexa-libros/', views.indexa_libros),
    path('indexa-libros-general/', views.indexa_librosGeneral),
    path('cargar-rs/', views.cargar_rs),
    path('indexa-ttl/', views.indexa_librosTtl),
    path('borrar/', views.borrar_bd),
    path('borrar-ttl/', views.borrar_ttl),
    path('carga-planeta-recomendados/', views.carga_planeta_recomendados),
    path('carga-planeta-nuevos/', views.carga_planeta_nuevos),
    #MOSTRADO DE DATOS
    path('', views.inicio),
    path('genero/<str:nombre_genero>', views.mostrar_genero),
    path('libros/<int:libro_id>',views.mostrar_libro),
    path('todostuslibros/', views.todostuslibros.as_view()),
    path('planetalibros/', views.planeta_libros),
    #BUSCADORES
    path('buscar-ttl/', views.buscadoresttl),
    path('buscador-general/',views.buscador_general),
    path('buscar/', views.buscadores),
    #RECOMENDACIONES
    path('recomendaciones/', views.recomendaciones),
    path('cargar-recomendacion-user/', views.ver_recomendaciones_user),
    path('todasrecomendaciones/', views.verRecomendacionesUsuarios),
    path('votacion/<int:page>',views.crear_usuarios_votantes),
    path('similares/<str:isbn>/', views.libros_similares),
    path('misvotaciones/<int:page>/', views.misvotaciones),
    #GESTION DE CUENTAS + ERROR GENERICO PARA LOS NO AUTENTIFICADOS O SUPERUSUARIOS
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', views.signup),
    path('error/', views.error),
]
