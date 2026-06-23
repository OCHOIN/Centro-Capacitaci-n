from django.contrib import admin
from .models import Perfil, Curso, Inscripcion, Certificado


admin.site.register(Perfil)
admin.site.register(Curso)
admin.site.register(Inscripcion)
admin.site.register(Certificado)