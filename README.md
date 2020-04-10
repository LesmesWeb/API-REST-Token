# API Rest Login Token

Este proyecto esta basado en la documentación de Django Rest con apoyo del tutorial de [Developer.pe](https://www.youtube.com/watch?v=kh4YFQrvVyE&list=PLMbRqrU_kvbRzgD2s7JHvJxGs6FdvFjg9&index=6) y mas adelante se implementara la documentación del API con la librería **coreapi** vale aclarar que hay se añadirán conocimientos que he adquirido.

## Configuraciones Iniciales

--En caso de iniciar el proyecto requiere de un entorno virtual e instalar lo siguiente:

```sh
-- sudo apt install virtualenv               #Paquete que habilitar la creación del entorno
-- virtualenv rest_env --python=python3      #Crea el entorno con python3
-- source rest_env/bin/activate              #Activar entorno
-- pip3 install -r requirements.txt          #Instalar paquetes pip3
```

- Crear proyecto y app
--django-admin startproject login_rest
--cd login_rest
--python3 manage.py startapp api

```sh
INSTALLED_APPS = [
 ...
 'rest_framework', #servicio rest
 'api', #app creada
]

TIME_ZONE = 'CO'  # America/Bogota (https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)
```

-- app/models.py

```sh
from django.db import models
class Persona(models.Model):
 id = models.AutoField(primary_key = True)
 nombre = models.CharField('Nombre',max_length=100)
 apellido = models.CharField('Apellido',max_length=50)

def __str__(self):
 return  '{0},{1}'.format(self.apellido,self.nombre)
class Meta:
 verbose_name = 'Persona'
 verbose_name_plural = 'Personas'
```

Registramos el modelo que creamos en el admin **api/admin.py**:

- python3 manage.py createsuperuser
-- admin
-- admin123

```sh
from django.contrib import admin
from .models import Persona

admin.site.register(Persona)

## Serializar

***Serialización***: Es el proceso de hacer una representación fluida de los datos que podemos transferir a través de la red. ***Deserialización*** es su proceso inverso.

 1. Creamos un archivo **api/serializers.py**: En se llamaran los campos del modelo a serializar con Json.
 2. Creamos un vista que muestre el listado de las personas registradas en la BD.
 3. Archivo de rutas para el API.
 4. Conectamos el APP con el proyecto.
 5. En el Setting damos permisos globales para que las clases rest no sean visualizadas sin primero logearse y por loggin con token

```sh
#Configuración global para todas las clases que existan en el proyecto

REST_FRAMEWORK = {
 'DEFAULT_PERMISSION_CLASSES':(
  'rest_framework.permissions.IsAuthenticated', #verificar si el usuario inicio sesión antes de acceder a una ruta del API
 ),
 'DEFAULT_AUTHENTICATION_CLASSES': (
  'rest_framework.authentication.TokenAuthentication', #Metodo de autenticación por TOKEN
 ),
}
```
