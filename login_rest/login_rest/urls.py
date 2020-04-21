"""login_rest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path,include
from rest_framework.authtoken import views
from api.views import Login,Logout
from rest_framework.documentation import include_docs_urls
from rest_framework_swagger.views import get_swagger_view
from rest_framework.authtoken import views

schema_view = get_swagger_view(title='Documentación API Vehiculos')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api_generate_token/',views.obtain_auth_token),

    path('',Login.as_view(), name = 'login'),
    path('logout/', Logout.as_view()),
    
    #enlazamos el archivo de ruta del app con el proyecto
    path('api/1.1/',include(('api.urls','api'))),
    
    #Urls de librerias de documentacion
    path('docs/', include_docs_urls(title='Documentación API Vehiculos')),
    path(r'documentacion/', schema_view), #Documentación Principal 
]