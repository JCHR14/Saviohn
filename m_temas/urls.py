from django.conf.urls import url
from m_temas import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include, re_path
 
urlpatterns = [
    path('temas-listado/', views.temas_listado, name='temas_listado'),
    path('temas-nuevo/', views.temas_nuevo, name='temas_nuevo'),
    path('temas-editar/<int:id>', views.temas_editar, name='temas_editar'),
    
    path('subtemas-listado/', views.subtemas_listado, name='subtemas_listado'),
    path('subtemas-nuevo/', views.subtemas_nuevo, name='subtemas_nuevo'),
    path('subtemas-editar/<int:id>', views.subtemas_editar, name='subtemas_editar'),

	path('reportes-listado/<int:subtema>', views.reportes_listado, name='reportes_listado'),  
	path('reportes-nuevo/<int:subtema>', views.reportes_nuevo, name='reportes_nuevo'),
    path('reportes-editar/<int:id>', views.reportes_editar, name='reportes_editar'),    

    url(r'^detalle-tema/(?P<codigo>\d+)/$', views.detalle_tema, name='detalle_tema'),
    #url(r'^suscribirse/$', views.suscribirse, name='suscribirse'),
    #url(r'^reportes/$', views.reportes, name='reportes'),
    #url(r'^salir/$', views.salir, name='salir'),
    #url(r'^perfil/$', views.perfil, name='perfil'),
]