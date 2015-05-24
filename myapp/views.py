# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect
import parserxml
import getData
from datetime import datetime, time
from django.contrib.auth import authenticate, login
from myapp.models import Actividad, Usuario, UsuarioActiv, UltimaActualiz
from myapp.models import ComentActiv
from django.template.response import TemplateResponse
from django.views.decorators.csrf import csrf_exempt
import rssCreate
from django.contrib.auth.models import User


# FUNCIONES ADICIONALES PARA SIMPLIFICAR


def filtrarPrevDia(request, actividades):
    try:
        dia = int(request.GET.get("prevdia"))
        mes = int(request.GET.get("prevmes"))
        ano = int(request.GET.get("prevano"))
        date = datetime(ano, mes, dia)
        actividadesfilt = actividades.filter(fecha__lte=date)
        return actividadesfilt
    except:
        return actividades


def filtrarPostDia(request, actividades):
    try:
        dia = int(request.GET.get("postdia"))
        mes = int(request.GET.get("postmes"))
        ano = int(request.GET.get("postano"))
        date = datetime(ano, mes, dia)
        actividadesfilt = actividades.filter(fecha__gte=date)
        return actividadesfilt
    except:
        return actividades


def filtrarTitle(request, actividades):
    try:
        if "title" in request.GET:
            title = request.GET["title"]
            actividadesfilt = actividades.filter(titulo__contains=title)
            return actividadesfilt
        else:
            return actividades
    except:
        return actividades


def filtrarPrecio(request, actividades):
    try:
        if "precio" in request.GET:
            precio = int(request.GET["precio"])
            actividadesfilt = actividades.filter(precio=precio)
            return actividadesfilt
        else:
            return actividades
    except:
        return actividades


# VISTAS APLICACION


def actividad(request, id):
    try:
        actividad = Actividad.objects.get(id=id)
        descripcion = getData.getMoreInfo(actividad.url)
        titulo = actividad.titulo
    except Actividad.DoesNotExist:
        descripcion = "Esta actividad no existe"
        actividad = None
        titulo = "No existe esta actividad"

    comentarios = ComentActiv.objects.filter(actividad=actividad)
    context = {'titulo': titulo,
               'descripcion': descripcion,
               'actividad': actividad,
               'request': request,
               'pagina': 'actividad',
               'comentarios': comentarios}
    return TemplateResponse(request, 'actividad.html', context)


def inicio(request):
    earlierActiv = []
    actividades = Actividad.objects.filter(
        fecha__gte=datetime.today()).order_by('fecha')

    for actividad in actividades:
        if len(earlierActiv) < 10:
            earlierActiv.append(actividad)

    context = {'titulo': "Inicio",
               'request': request,
               'usuarios': Usuario.objects.all(),
               'actividades': earlierActiv,
               'pagina': 'inicio'}
    return TemplateResponse(request, 'inicio.html', context)


def todas(request, filtrado):
    actividades = Actividad.objects.all()
    actividadesFilt = filtrarPrevDia(request, actividades)
    actividadesFilt = filtrarPostDia(request, actividadesFilt)
    actividadesFilt = filtrarTitle(request, actividadesFilt)
    actividadesFilt = filtrarPrecio(request, actividadesFilt)

    try:
        lastupdate = UltimaActualiz.objects.get(id=1)
        fechaUltima = lastupdate.fecha
    except:
        fechaUltima = "No conocida"

    context = {'titulo': "Todas las actividades",
               'actividades': actividadesFilt,
               'request': request,
               'last_update': fechaUltima,
               'pagina': 'todas'}
    return TemplateResponse(request, 'todas.html', context)


def actualizar(request):
    listOfContents = parserxml.getListEvents(
        "http://datos.madrid.es/egob/catalogo/206974-0-agenda-eventos-culturales-100.xml")

    for dicc in listOfContents:
        try:
            titulo = dicc['TITULO']
        except KeyError:
            titulo = "no indicado"
        try:
            tipo = dicc['TIPO']
        except KeyError:
            tipo = "no indicado"
        try:
            fecha = datetime.strptime(dicc['FECHA-EVENTO'], "%Y-%m-%d")
        except KeyError:
            fecha = datetime.strptime("2011-06-25", "%Y-%m-%d")
        try:
            horaminuto = dicc['HORA-EVENTO'].split(":")
            hora = time(int(horaminuto[0]), int(horaminuto[1]))
        except KeyError:
            hora = time(0, 0)
        try:
            urlinfo = dicc['CONTENT-URL']
        except KeyError:
            urlinfo = "no indicada"
        try:
            if dicc['EVENTO-LARGA-DURACION']:
                larga = "si"
            else:
                larga = "no"
        except KeyError:
            larga = "no indicado"
        try:
            precio = int(dicc['PRECIO'].split()[0])
        except:
            precio = 0
        try:
            Actividad.objects.get(titulo=titulo, tipo=tipo, fecha=fecha,
                                  hora=hora, url=urlinfo)
        except Actividad.DoesNotExist:
            activ = Actividad(titulo=titulo, tipo=tipo, fecha=fecha, hora=hora,
                              url=urlinfo, larga_duracion=larga, precio=precio)
            activ.save()
    try:
        prevAct = UltimaActualiz.objects.get(id=1)
        prevAct.fecha = datetime.now()
        prevAct.save()
    except UltimaActualiz.DoesNotExist:
        last = UltimaActualiz(fecha=datetime.now())
        last.save()
    return HttpResponseRedirect("/todas")


@csrf_exempt
def usuario(request, nombre):
    if request.method == "GET":
        try:
            page = int(request.GET.get("page"))
        except TypeError:
            page = 0

        actividadesUser = UsuarioActiv.objects.filter(usuario__nombre=nombre)
        actividades = []
        try:
            usuarioPagina = Usuario.objects.get(nombre=nombre)
        except Usuario.DoesNotExist:
            usuarioPagina = None

        if usuarioPagina:
            campoSesion = 'visitado_' + nombre
            # solo aumenta el contador una vez por sesión
            if not request.session.get(campoSesion, False):
                request.session[campoSesion] = True
                usuarioPagina.visitasPerfill += 1
                usuarioPagina.save()
            if usuarioPagina.titulo == "":
                titulo = u"Página de " + nombre
            else:
                titulo = usuarioPagina.titulo
        else:
            titulo = "Usuario no encontrado"

        numActiv = 1
        for actividadUser in actividadesUser:
            if (numActiv > page * 10) and (numActiv <= page * 10 + 10):
                actividades.append(actividadUser.actividad)
            numActiv += 1

        num_pags = len(actividadesUser) / 10
        if (len(actividadesUser) % 10) > 0:
            num_pags += 1

        context = {'titulo': titulo,
                   'actividades': actividades,
                   'numRangePag': range(num_pags),
                   'UsuarioPagina': usuarioPagina,
                   'pagina': 'usuario',
                   'request': request}
        return TemplateResponse(request, 'usuario.html', context)

    # Añadir una nueva actividad
    elif request.method == "POST" and nombre == request.user.username:
        if "id" in request.POST and request.POST["id"]:
            id = request.POST["id"]
            user = Usuario.objects.get(nombre=nombre)
            actividad = Actividad.objects.get(id=id)
            fecha = datetime.now()
            try:
                UsuarioActiv.objects.get(usuario=user, actividad=actividad)
                salida = "Ya estaba agregada"
            except UsuarioActiv.DoesNotExist:
                activ = UsuarioActiv(
                    usuario=user, actividad=actividad, ingresado=fecha)
                activ.save()
                salida = "agregada"
        else:
            salida = "No puedes agregarla"
        return HttpResponse(salida)
    else:
        return HttpResponseRedirect("/todas")


def ayuda(request):

    context = {'titulo': "Ayuda",
               'pagina': 'ayuda',
               'request': request}
    return TemplateResponse(request, 'ayuda.html', context)


def rssUser(request, nombre):
    actividadesUser = UsuarioActiv.objects.filter(usuario__nombre=nombre)
    contentRSS = rssCreate.userRSS(actividadesUser, nombre)
    return HttpResponse(contentRSS, content_type="application/rss+xml")


def rssInicio(request):
    earlierActiv = []
    actividades = Actividad.objects.filter(
        fecha__gte=datetime.today()).order_by('fecha')

    for actividad in actividades:
        if len(earlierActiv) < 10:
            earlierActiv.append(actividad)
    contentRSS = rssCreate.inicioRSS(earlierActiv)
    return HttpResponse(contentRSS, content_type="application/rss+xml")


def parametrosUser(request, nombre):
    if request.method == 'POST':
        if nombre == request.user.username:
            usuario = Usuario.objects.get(nombre=nombre)
            if "title" in request.POST and request.POST["title"]:
                title = request.POST["title"]
            else:
                title = ""

            if "descripcion" in request.POST and request.POST["descripcion"]:
                descripcion = request.POST["descripcion"]
            else:
                descripcion = ""

            if "size" in request.POST and request.POST["size"]:
                sizeFuente = request.POST["size"]

            if "color" in request.POST and request.POST["color"]:
                colorFuente = request.POST["color"]

            if "background" in request.POST and request.POST["background"]:
                backColor = request.POST["background"]

            usuario.titulo = title
            usuario.descripcion = descripcion
            usuario.sizeFuente = sizeFuente
            usuario.colorFuente = colorFuente
            usuario.backColor = backColor
            usuario.save()
            return HttpResponseRedirect('/' + nombre)
        else:
            # No es su pagina, no puede hacer post
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/' + nombre)


def formatCSS(request, namecss):
    if request.user.is_authenticated():
        try:
            usuario = Usuario.objects.get(nombre=request.user.username)
        except:
            return TemplateResponse(request, 'css/main.css', content_type="text/css")
        context = {'backcolor': usuario.backColor,
                   'colorFuente': usuario.colorFuente,
                   'sizeFuente': usuario.sizeFuente,
                   }
        return TemplateResponse(request, 'css/main.css', context,
                                content_type="text/css")
    else:
        return TemplateResponse(request, 'css/main.css', content_type="text/css")


def registrar(request):
    error = None
    if request.method == "POST":
        nombre = request.POST.get('nombre', None)
        password = request.POST.get('password', None)
        titulo = request.POST.get('titulo', None)
        descripcion = request.POST.get('descripcion', None)

        if nombre and password:
            try:
                User.objects.get(username=nombre)
                error = "Ese usuario ya existe"
            except:
                user = User.objects.create_user(
                    username=nombre, password=password)
                user.save()
                user = authenticate(username=nombre, password=password)
                login(request, user)
                userCaract = Usuario(
                    nombre=nombre, titulo=titulo, descripcion=descripcion)
                userCaract.save()

                return HttpResponseRedirect("/" + nombre)
        else:
            error = "Los campos marcados con * son obligatorios"

    context = {'titulo': 'Registrate',
               'pagina': 'registro',
               'request': request,
               'error': error}
    return TemplateResponse(request, 'registro.html', context)


# Permitir a usuarios no registrados valorar, luego
# un solo voto por sesión
@csrf_exempt
def valorarActividad(request, idActividad):
    if request.method == 'POST':
        campoSesion = 'valoradoActiv' + idActividad
        if request.session.get(campoSesion, False):
            respuesta = "Ya la valoraste"
        else:
            try:
                actividad = Actividad.objects.get(id=idActividad)
                actividad.valoracion += 1
                actividad.save()
                request.session[campoSesion] = True
                respuesta = "Gracias por valorar"
            except Actividad.DoesNotExist:
                respuesta = "La actividad indicada no existe"

        return HttpResponse(respuesta)

    else:
        context = {'titulo': 'Valorar actividad',
                   'pagina': 'valorar actividad',
                   'request': request,
                   'error': "Solo POST sobre este recurso"}
    return TemplateResponse(request, 'index2.html', context)


@csrf_exempt
def comentarActividad(request, idActividad):
    if request.method == 'POST':
        try:
            actividad = Actividad.objects.get(id=idActividad)
            usuario = Usuario.objects.get(nombre=request.user.username)
            contenido = request.POST.get('comentario', None)
            if usuario and contenido and actividad:
                comentario = ComentActiv(
                    usuario=usuario, comentario=contenido, actividad=actividad)
                comentario.save()
        except Actividad.DoesNotExist:
            print ""

    return HttpResponseRedirect("/actividad/" + idActividad)
