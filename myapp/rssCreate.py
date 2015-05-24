# -*- coding: utf-8 -*-


def formatActividad(actividad):
    salida = '<item>'
    salida += '<title>' + actividad.titulo + '</title>'
    salida += '<link>http://localhost:8000/actividad/' + \
        str(actividad.id) + '</link>'
    salida += '<largaDuracion>' + \
        str(actividad.larga_duracion) + '</largaDuracion>'
    salida += '<fechaEvento>' + str(actividad.fecha) + '</fechaEvento>'
    salida += '<horaEvento>' + str(actividad.hora) + '</horaEvento>'
    salida += '<tipoEvento>' + actividad.tipo + '</tipoEvento>'
    salida += '<precioEvento>' + str(actividad.precio) + '</precioEvento>'
    salida += '</item>'
    return salida


def inicioRSS(actividades):
    salida = '<?xml version="1.0" encoding="UTF-8" ?>\n'
    salida += '<rss version="2.0">\n'
    salida += u'<title>Próximas actividades en Madrid</title>'
    salida += u'<description>Listado de las próximas 10 actividades ' +\
        u'que tendrán lugar en Madrid durante los próximos días</description>'
    salida += '<channel>\n'
    for actividad in actividades:
        salida += formatActividad(actividad)
    salida += '</channel>'
    salida += '</rss>'
    return salida


def userRSS(activitiesUser, nombre):
    salida = '<?xml version="1.0" encoding="UTF-8" ?>'
    salida += '<rss version="2.0">'
    salida += '<channel>'
    salida += '<title>RSS de ' + nombre + '</title>'
    salida += '<description>Actividades seleccionadas</description>'
    salida += '<link>localhost:8000/' + nombre + '</link>'
    for activityUser in activitiesUser:
        actividad = activityUser.actividad
        salida += formatActividad(actividad)
    salida += '</channel>'
    salida += '</rss>'
    return salida
