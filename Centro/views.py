from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.db.models import Avg, Count

from .models import Perfil, Curso, Inscripcion, Certificado

def index(request):
    return render(request, 'index.html')


def indexinstr(request):
    return render(request, 'indextr.html')

def indexest(request):
    return render(request, 'indexest.html')

def registro(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        tipo_usuario = request.POST.get('tipo_usuario')

        if User.objects.filter(username=username).exists():
            messages.error(request, "El usuario ya existe")
            return render(request, 'registro.html')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        Perfil.objects.create(
            usuario=user,
            tipo_usuario=tipo_usuario
        )

        messages.success(request, "Registro exitoso")
        return render(request, 'registro.html', {'registro_exitoso': True})

    return render(request, 'registro.html')

def login_r(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            try:
                perfil = Perfil.objects.get(usuario=user)

                if perfil.tipo_usuario == "instructor":
                    return redirect('/indexinstr/')
                elif perfil.tipo_usuario == "alumno":
                    return redirect('/indexest/')
                else:
                    messages.error(request, "No tiene permisos")

            except Perfil.DoesNotExist:
                messages.error(request, "Perfil no encontrado")

        else:
            messages.error(request, "Usuario o contraseña incorrectos")

    return render(request, 'login.html')

def listarCursos(request):
    cursos = Curso.objects.all()
    return render(request, 'Cursos.html', {'cursos': cursos})

def nuevoCurso(request):

    if request.method == "POST":

        curso = Curso(
            nombre=request.POST["nombre"],
            modalidad=request.POST["modalidad"],
            categoria=request.POST["categoria"],
            fecha_lanzamiento=request.POST["fecha"],
            foto=request.FILES.get("foto"),

            material_descargable=True if request.POST.get("material") else False,

            instructor=request.user
        )

        curso.save()

        messages.success(request, "Curso agregado correctamente")
        return redirect("/cursos/")

    return render(request, "NuevoCurso.html")

def editarCurso(request, id):

    curso = get_object_or_404(Curso, id=id)

    if request.method == 'POST':

        if not request.FILES.get('foto') and not curso.foto:
            messages.error(request, "Debe seleccionar una imagen.")
            return render(request,'editarCurso.html',{
                'curso':curso
            })

        curso.nombre_curso = request.POST['nombre']
        curso.modalidad = request.POST['modalidad']
        curso.categoria = request.POST['categoria']
        curso.fecha_lanzamiento = request.POST['fecha']

        if request.FILES.get('foto'):
            curso.foto = request.FILES.get('foto')

        curso.material_descargable = True if request.POST.get("material") else False

        curso.save()

        messages.success(request, "Curso actualizado")
        return redirect('/cursos/')

    return render(request,'editarCurso.html',{
        'curso':curso
    })

def eliminarCurso(request, id):

    curso = get_object_or_404(Curso, id=id)

    # BORRAR ARCHIVO DE IMAGEN
    if curso.foto:
        curso.foto.delete(save=False)

    # BORRAR REGISTRO
    curso.delete()

    messages.success(request, "Curso eliminado")
    return redirect('/cursos/')

def inscripcion(request):

    cursos = Curso.objects.all()
    inscripciones = Inscripcion.objects.filter(alumno=request.user)

    return render(request, 'inscripcion.html', {
        'cursos': cursos,
        'inscripciones': inscripciones
    })

def nuevaInscripcion(request):

    if request.method == 'POST':

        curso_id = request.POST['curso']

        # VERIFICAR SI YA ESTÁ INSCRITO
        existe = Inscripcion.objects.filter(
            alumno=request.user,
            curso_id=curso_id
        ).exists()

        if existe:
            messages.error(request, "Ya estás inscrito en este curso")
            return redirect('/inscripciones/')

        # CREAR INSCRIPCIÓN
        Inscripcion.objects.create(
            alumno=request.user,
            curso_id=curso_id
        )

        messages.success(request, "Inscripción realizada")
        return redirect('/inscripciones/')

def eliminarInscripcion(request, id):

    inscripcion = get_object_or_404(Inscripcion, id=id, alumno=request.user)
    inscripcion.delete()

    messages.success(request, "Inscripción eliminada")
    return redirect('/inscripciones/')

def listarCertificados(request):

    certificados = Certificado.objects.all()

    return render(request, 'Certificados.html', {
        'certificados': certificados
    })

def nuevoCertificado(request):

    if request.method == 'POST':

        alumno_id = request.POST.get('alumno')
        curso_id = request.POST.get('curso')

        # Validación básica
        if not alumno_id or not curso_id:
            messages.error(request, "Seleccione alumno y curso")
            return redirect('/nuevoCertificado/')

        # Verificar matrícula
        if not Inscripcion.objects.filter(
            alumno_id=alumno_id,
            curso_id=curso_id
        ).exists():
            messages.error(request, "El alumno no está matriculado en este curso")
            return redirect('/nuevoCertificado/')

        # Crear certificado
        Certificado.objects.create(
            alumno_id=alumno_id,
            curso_id=curso_id,
            fecha_emision=request.POST.get('fecha_emision'),
            calificacion_final=request.POST.get('calificacion'),
            estado_documento=request.POST.get('estado'),
            archivo_pdf=request.FILES.get('archivo_pdf')
        )

        messages.success(request, "Certificado generado correctamente")
        return redirect('/certificados/')

    cursos = Curso.objects.all()

    inscripciones = Inscripcion.objects.select_related('alumno', 'curso')

    return render(request, 'nuevoCertificado.html', {
        'cursos': cursos,
        'inscripciones': inscripciones
    })

def editarCertificado(request, id):

    certificado = get_object_or_404(Certificado, id=id)

    if request.method == 'POST':

        certificado.alumno_id = request.POST['alumno']
        certificado.curso_id = request.POST['curso']
        certificado.fecha_emision = request.POST['fecha_emision']
        certificado.calificacion_final = request.POST['calificacion']
        certificado.estado_documento = request.POST['estado']

        if request.FILES.get('archivo_pdf'):
            certificado.archivo_pdf = request.FILES.get('archivo_pdf')

        certificado.save()

        messages.success(request, "Certificado actualizado")
        return redirect('/certificados/')

    return render(request, "editarCertificado.html", {
        "certificado": certificado,
        "cursos": Curso.objects.all(),
        "inscripciones": Inscripcion.objects.select_related('alumno', 'curso')
    })

def eliminarCertificado(request, id):

    certificado = get_object_or_404(Certificado, id=id)

    # BORRAR ARCHIVO FÍSICO
    if certificado.archivo_pdf:
        certificado.archivo_pdf.delete(save=False)

    # BORRAR REGISTRO
    certificado.delete()

    messages.success(request, "Certificado eliminado")
    return redirect('/certificados/')

def misCertificados(request):

    certificados = Certificado.objects.filter(
        alumno=request.user
    )

    return render(request, 'CertificadosEst.html', {
        'certificados': certificados
    })



def evaluarCurso(request):

    # =========================
    # PROMEDIO POR CURSO
    # =========================
    cursos = Curso.objects.all()

    promedios = []

    for curso in cursos:

        promedio = Certificado.objects.filter(
            curso=curso
        ).aggregate(promedio=Avg('calificacion_final'))['promedio']

        promedios.append({
            'nombre': curso.nombre,
            'promedio': promedio or 0
        })

    # =========================
    # EFICIENCIA
    # =========================
    eficiencia = []

    for curso in cursos:

        inscritos = Inscripcion.objects.filter(curso=curso).count()
        certificados = Certificado.objects.filter(curso=curso).count()

        porcentaje = 0
        if inscritos > 0:
            porcentaje = (certificados / inscritos) * 100

        eficiencia.append({
            'curso': curso.nombre,
            'inscritos': inscritos,
            'certificados': certificados,
            'porcentaje': round(porcentaje, 2)
        })

    return render(request, 'EvaluarCurso.html', {
        'promedios': promedios,
        'eficiencia': eficiencia
    })


def cursosDisponibles(request):
    cursos = Curso.objects.all()

    return render(request, 'cursoEstudiante.html', {
        'cursos': cursos
    })