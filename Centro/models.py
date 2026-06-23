from django.db import models
from django.contrib.auth.models import User


# ======================================================
# PERFIL DE USUARIO
# ======================================================

class Perfil(models.Model):

    TIPOS_USUARIO = (
        ('instructor', 'Instructor'),
        ('alumno', 'Alumno'),
    )

    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo_usuario = models.CharField(max_length=20, choices=TIPOS_USUARIO)

    def __str__(self):
        return f"{self.usuario.username} - {self.tipo_usuario}"


# ======================================================
# CURSOS
# ======================================================

class Curso(models.Model):

    MODALIDAD_CHOICES = (
        ('presencial', 'Presencial'),
        ('en_linea', 'En Línea'),
    )

    CATEGORIA_CHOICES = (
        ('tecnologia', 'Tecnología'),
        ('idiomas', 'Idiomas'),
        ('negocios', 'Negocios'),
    )

    nombre = models.CharField(max_length=200)
    foto = models.ImageField(upload_to='cursos/', null=True, blank=True)
    modalidad = models.CharField(max_length=20, choices=MODALIDAD_CHOICES)
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES)
    fecha_lanzamiento = models.DateField()
    material_descargable = models.BooleanField(default=False)

    instructor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='cursos_creados',
        limit_choices_to={'perfil__tipo_usuario': 'instructor'}
    )

    def __str__(self):
        return self.nombre


# ======================================================
# INSCRIPCIONES
# ======================================================

class Inscripcion(models.Model):

    alumno = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='inscripciones',
        limit_choices_to={'perfil__tipo_usuario': 'alumno'}
    )

    curso = models.ForeignKey(
        Curso,
        on_delete=models.CASCADE,
        related_name='inscripciones'
    )

    fecha_inscripcion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.alumno.username} - {self.curso.nombre}"


# ======================================================
# CERTIFICADOS
# ======================================================

from django.contrib.auth.models import User

class Certificado(models.Model):

    ESTADO_CHOICES = (
        ('original', 'Original'),
        ('duplicado', 'Duplicado'),
    )

    alumno = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='certificados',
        null=True,
        blank=True
    )

    curso = models.ForeignKey(
        Curso,
        on_delete=models.CASCADE,
        related_name='certificados'
    )

    archivo_pdf = models.FileField(
        upload_to='certificados/'
    )

    fecha_emision = models.DateField()

    calificacion_final = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )

    estado_documento = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES
    )

    def __str__(self):
        return f"{self.alumno.username} - {self.curso.nombre}"