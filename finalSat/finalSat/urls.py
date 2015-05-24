from django.conf.urls import patterns, include, url
from django.contrib import admin
from finalSat.feed import feed
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'finalSat.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^(?P<usuario>.*)/rss$', feed()),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'EventosMadrid.views.principal'),
    url(r'^actividades/(.*)$', 'EventosMadrid.views.infoActividad'),
    url(r'^todas/$', 'EventosMadrid.views.todas'),
    url(r'^loguear/$', 'EventosMadrid.views.loguear'),
    url(r'^expulsar/$', 'EventosMadrid.views.expulsar'),
    url(r'^actualizar/$', 'EventosMadrid.views.actualizar'),
    url(r'^cambioTitulo$', 'EventosMadrid.views.cambioTitulo'),
    url(r'^seleccionar/(.*)$', 'EventosMadrid.views.seleccionar'),
    url(r'^ayuda/$', 'EventosMadrid.views.ayuda'),
    url(r'^(.*)$', 'EventosMadrid.views.pagUsuario'),

)
