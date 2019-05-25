from django.conf.urls import url
from m_usuarios import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include, re_path
 
urlpatterns = [
    path('grupos-listado/', views.grupos_listado, name='grupos_listado'),
    path('grupos-crear/', views.grupos_crear, name='grupos_crear'),
    path('grupos-editar/<int:id>/', views.grupos_editar, name='grupos_editar'),
    path('usuarios-listado/', views.usuarios_listado, name='usuarios_listado'), 
    path('usuarios-detalle/<int:id>', views.usuarios_detalle, name='usuarios_detalle'),
    path('usuarios-reset-pwd/<int:id>/', views.usuarios_reset_pwd, name='usuarios_reset_pwd'),
]