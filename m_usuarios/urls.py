from django.conf.urls import url
from m_usuarios import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include, re_path
 
urlpatterns = [
    #path('temas-listado/', views.temas_listado, name='temas_listado'),
    #path('temas-nuevo/', views.temas_nuevo, name='temas_nuevo'),
    #path('temas-editar/<int:id>', views.temas_editar, name='temas_editar'),
    #url(r'^detalle-tema/(?P<codigo>\d+)/$', views.detalle_tema, name='detalle_tema'),
    #url(r'^suscribirse/$', views.suscribirse, name='suscribirse'),
    #url(r'^reportes/$', views.reportes, name='reportes'),
    #url(r'^salir/$', views.salir, name='salir'),
    #url(r'^perfil/$', views.perfil, name='perfil'),
    
    #path('usuarios-listado/', views.usuarios_listado, name='usuarios_listado'),
    #path('usuarios-crear/', views.usuarios_crear, name='usuarios_crear'),
    #path('usuarios-editar/<int:id>', views.usuarios_editar, name='usuarios_editar'),

    path('grupos-listado/', views.grupos_listado, name='grupos_listado'),
    path('grupos-crear/', views.grupos_crear, name='grupos_crear'),
    path('grupos-editar/<int:id>/', views.grupos_editar, name='grupos_editar'),

    
	#url(r'^listado-usuarios/$', views.listado_usuarios, name='listado_usuarios'),
    #url(r'^crear-usuario/$', views.crear_usuario, name='crear_usuario'),
    #url(r'^editar-usuario/(?P<codigo>\d+)/$', views.editar_usuario, name='editar_usuario'),
    #url(r'^listado-grupos/$', views.listado_grupos, name='listado_grupos'),
    #url(r'^crear-grupo/$', views.crear_grupo, name='crear_grupo'),
    #url(r'^editar-grupo/(?P<codigo>\d+)/$', views.editar_grupo, name='editar_grupo'),
  
]