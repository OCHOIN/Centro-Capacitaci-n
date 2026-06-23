from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    # principales
    path('', views.index),
    path('indexinstr/', views.indexinstr),
    path('indexest/', views.indexest),

    # auth
    path('registro/', views.registro),
    path('login/', views.login_r),

    # cursos
    path('cursos/', views.listarCursos),
    path('nuevoCurso/', views.nuevoCurso),
    path('editarCurso/<int:id>/', views.editarCurso),
    path('eliminarCurso/<int:id>/', views.eliminarCurso),
    path('cursosDisponibles/', views.cursosDisponibles),

    # inscripciones
    path('inscripciones/', views.inscripcion),
    path('inscribir/', views.nuevaInscripcion),
    path('eliminarInscripcion/<int:id>/', views.eliminarInscripcion),
    path('Miscertificados/', views.misCertificados),

    # certificados
    path('certificados/', views.listarCertificados),
    path('nuevoCertificado/', views.nuevoCertificado),
    path('certificadoeliminar/<int:id>/', views.eliminarCertificado),
    path('certificadoeditar/<int:id>/', views.editarCertificado),

    # reportes
    path('evaluarCurso/', views.evaluarCurso),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)