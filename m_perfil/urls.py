from django.conf.urls import url
from m_perfil import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include, re_path
 
urlpatterns = [
    #path('activate/<slug:uidb64>/<slug:token>/', views.activate, name='activate'),
    path('', views.perfil, name='perfil'),
    path('cambiar-password/', views.change_password, name='change_password'),
    #url(r'^cambiar-password/$', views.change_password, name='change_password'),
    #url(r'^activate/(?P<uidb64>.+)/(?P<token>.+)/$',views.activate, name='activate'),
    
]