from django.contrib import admin
from myapp.models import Actividad, Usuario, UsuarioActiv, UltimaActualiz, ComentActiv

# Register your models here.
admin.site.register(Actividad)
admin.site.register(Usuario)
admin.site.register(UsuarioActiv)
admin.site.register(UltimaActualiz)
admin.site.register(ComentActiv)
