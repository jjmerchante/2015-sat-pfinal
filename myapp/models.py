from django.db import models


class Actividad(models.Model):
    titulo = models.TextField()
    larga_duracion = models.CharField(max_length=24)
    fecha = models.DateField()
    hora = models.TimeField()
    tipo = models.TextField()
    url = models.URLField()
    precio = models.IntegerField()
    valoracion = models.PositiveIntegerField(default=0)


class Usuario(models.Model):
    nombre = models.CharField(max_length=128)
    titulo = models.CharField(max_length=256)
    descripcion = models.TextField()
    colorFuente = models.CharField(max_length=64, default="#333")
    sizeFuente = models.IntegerField(default=11)
    backColor = models.CharField(max_length=64, default="#FFF")
    visitasPerfill = models.PositiveIntegerField(default=0)


class UsuarioActiv(models.Model):
    usuario = models.ForeignKey(Usuario)
    actividad = models.ForeignKey(Actividad)
    ingresado = models.DateField()


class UltimaActualiz(models.Model):
    fecha = models.DateField()


class ComentActiv(models.Model):
    usuario = models.ForeignKey(Usuario)
    actividad = models.ForeignKey(Actividad)
    comentario = models.TextField()
