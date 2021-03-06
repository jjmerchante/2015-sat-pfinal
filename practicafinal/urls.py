from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^todas(.*)', 'myapp.views.todas'),
                       url(r'^$', 'myapp.views.inicio'),
                       url(r'^actividad/(\d+)$', 'myapp.views.actividad'),
                       url(r'^ayuda$', 'myapp.views.ayuda'),
                       url(r'^actualizar$', 'myapp.views.actualizar'),
                       url(r'^css/(.+)$', 'myapp.views.formatCSS'),
                       url(r'^files/(?P<path>.*)$',
                           'django.views.static.serve',
                           {'document_root': 'files'}),
                       url(r'^logout$', 'django.contrib.auth.views.logout',
                           {'next_page': '/'}),
                       url(r'^login$', 'django.contrib.auth.views.login'),
                       url(r'^rss$', 'myapp.views.rssInicio'),
                       url(r'^(.*)/rss$', 'myapp.views.rssUser'),
                       url(r'^(.*)/parametros$', 'myapp.views.parametrosUser'),
                       url(r'^registrar$', 'myapp.views.registrar'),
                       url(r'^actividad/(\d+)/valorar$',
                           'myapp.views.valorarActividad'),
                       url(r'^actividad/(\d+)/comentario$',
                           'myapp.views.comentarActividad'),
                       url(r'^(favicon.ico)$', 'django.views.static.serve',
                           {'document_root': 'files/images'}),
                       url(r'^(.*)', 'myapp.views.usuario'),
                       )
