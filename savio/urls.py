"""savio URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls.static import static
from django.conf.urls import handler404, handler500, url, include
from django.conf import settings
from django.contrib.auth import views as auth_views 
from m_generales import views as vw

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^login/$', auth_views.LoginView.as_view(), {'template_name': 'ingreso.html'}, name='login'),
    #path('perfil/change-password/',auth_views.PasswordChangeView.as_view(), {'template_name':'change-password.html'}, name="cambio_password"),
    path('', include('m_generales.urls')),
    path('temas/', include('m_temas.urls')),
    path('perfil/', include('m_perfil.urls')),
    path('usuarios/', include('m_usuarios.urls')),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = vw.handler404
handler500 = vw.handler500