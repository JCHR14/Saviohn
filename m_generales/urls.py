from django.conf.urls import url
from m_generales import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include, re_path
 
urlpatterns = [
    url(r'^$', views.inicio, name='inicio'),
    url(r'^suscribirse/$', views.suscribirse, name='suscribirse'),
    url(r'^nuestros-planes/$', views.nuestros_planes, name='nuestros_planes'),
    url(r'^reportes/$', views.reportes, name='reportes'),
    url(r'^salir/$', views.salir, name='salir'),
    url(r'^quien-soy/$', views.quien_soy, name='quien_soy'),
    url(r'^contacto/$', views.contacto, name='contacto'), 
    url(r'^activate/(?P<uidb64>.+)/(?P<token>.+)/$',views.activate, name='activate'),
    url(r'^reset-password/$', views.reset_password, name='reset_password'),
]
