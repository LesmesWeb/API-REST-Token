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

## Token authentication

DJANGO ya trae en su nucleo la creación de tokens automaticos:
-- En settings.py añadir la aplicación que permite la creación de las tablas token

```sh
INSTALLED_APPS = [
 ...
 'rest_framework.authtoken', #aplicación para generar la tabla tokens 
]
```

-- realizar migraciones: **python3 manage.py migrate**
-- ingresaremos al proyecto y en urls: **login_rest/urls.py** 

```sh
urlpatterns = [
 ...
 #generador de tokens de usuario estos deben ser via POST (Se puede validar en Postman)
 path('api_generate_token/',views.obtain_auth_token),
]
```

Con **Postman** se podra hacer la validación de los dos campos requeridos en método Post:
![Postman validación](https://lh3.googleusercontent.com/Vm6M3Nd0aXqdGANjlt1jo59QvLfQnaY5lp2w-5uKGot16L3M8TNXpm8Mk3QBI42jtlMEl6Ik0Lro0kNdnShv32QYf51Z9yVnSAlFJRpML1YJQIYncb9SjEComyiqev-v0bC3pNSlrnTX4CC8W-caPtkmRzlS0ogQBSZYzMB5eYXrt_vQq-BmSImJUaM8XhUw-l2LoxMPAonwKltQLYs_XGf23LodK7hJ9ngQscALa8XF6dUyPuMO-bArmyjmNsH_b9Niy86hGGjC6hKbfvejDnpdRkYJ2-bcnrKn5yWEcFIjmRIGIS8H8cx3-22uuPDJAk4c87U7zEtN4bipfiikyV6kFrSv2JD6kyDhxAP4SaL3_h_JRZ0pzmq24gcWF5oDGh5QyHEaEWR_lG354ui4spVG6yTfIWGxerb2MfMBtz87zSzp0010WBiRr2C7f9qJl-hy0O1uSWXIG3WwfFiLPrTT-1VdAWD2pZDhFYPd887RXUO-TyymdizIL6HigM8QOlWbsUTyBjKB6cK3FhZv-Nzbi7O3laVnC_1sSjJB9RVxkHBkFXCel2KT6eLR3m8mOEdQdWhUifieVJ92Tm9XdCv3ebEaiSSOy28fNP3WWY3lhQbHYl5pAfhc14PVBFGlKI844giU_ZcehYv1o8pSPmzUKPGXXvzjexZ2LKRY7xIgZcMQY7Buj4KEStgH0A=w993-h604-no)

Otra herramienta para realizar la validación es **httpie**para validar por se requiere instalar.
-- pip3 install httpie
-- Para ejecutar por POST con esa libreria y general token se hace de la siguiente manera:

```sh
http http://localhost:8000/api_generate_token/ username="admin" password="admin123"
```

![httpie validación](https://lh3.googleusercontent.com/-wdSDq0fDuNh2dndNhVttt2k2JOijo9JU1LmdF0b0wF9ZykVE3xi5k8qbVadOLFQxQWn7SZeO_HsBI42NS0jsEppqfkfXEpXms_veUVeIpUrhBpmfdvwjz8Lm501bZPoB01-OO7HUXAgSeYxalV6UDdR90GFfTr75g5QMsOxwfljxNNKzZxLIV88SvI-MHBby4WJ7XJPJUKlFaspKBSUtWSK0cNWvwZs_Rha1iTjpUaZTQtvx2Oc1fSB7Coqx_kZApDuBpivvTAvUu477OH7R4yn8pnrM18cSJBdMrjW1roORbQBfqTBcaT5MMzBjK4c-RjlrKRBJSn5KG03MQ5sU4G0XeKsMGO86P3WnXOxqM5LnxK_Z3sTTV-9G8mkV_Ahwb5RX0viKAhOADx9Qb2BKcKzv_G5WsxMmxVDXSEmVXZictZNPpcablfjdwYGt1GAxh3VY7SwN2oKaDW-B5QACnFGmxXSiHvJKUuMyDm3QHAw7XaZKVxYgajBiQ0USAILPUojXAp-cuFV4mguBP1kWKg_RZJWtnnCbpFD6ugTgyjyKkGb03UT4eSz4xQYPCxbRWeAHK_Mi2EJ2HGt5Xbf8tCAfb7qT-gn5oSurZTOgKtSsOUnpwVW97l7RUgDXtaQTv0pL8W8QQ4bwqJbfIoXOivZKnJZDnZ_N2-iFmcHudvfPTHrMBSNG3pmyuLc0SvcYeQ9lYf8A1Rw5WRUbsv-H-DST9hicy1tZ6hFsyJbu7RGIRvf-wttbN0=w1174-h250-no)

<hr>

### Token en lista de personas

Es necesario que ahora nuestra lista de persona en la url [http://localhost:8000/api/1.0/persona/](http://localhost:8000/api/1.0/persona/) permite la autenticación buscando el token automáticamente.

De la manera manual seria de esta manera con **httpie**:

```sh
http http://localhost:8000/api/1.0/persona/ "Authorization: Token 62c36405d4927915d24afd1b0baeb1931183b052"
```

En **Postman** seria de la siguiente manera:
![postman validación lista de personas](https://lh3.googleusercontent.com/KIndtpZ-81yiBIf2yKjfkw0KhBo915SooU4D3TrQvY6-E8dou_uXvrrPPAuFbN9Wxpv5VmknghoyGrrktIXO1W7Dl4ltFwo7x7RHqcb3rmWJuXbVDkjB6UwOIZi1Uj-f_6hmWYnwYe8U1Wpw9-bXUXjXGpMe_D0biouX5ZeAM1rrH8khfwYNZAuOHohmkK7nR4J1vE7vD5xmBMkexBIeZc2-Vzxw_CI35ZKvJ7jsx0Qp2BdRw-jHoQgx2o8e23TiS6Ra3gazz5oF4uZXc7UrSMcFHK6egDgY7yhkW2gxfrnBHJfkNtq1GmgFvzMKNOjqLB4td3_megcZE7-AQuiz_kHDTBgRqvbRXC-EiRgfTT6Xr8qCTL5ffGfeWoGzwv3W52zl8Uz15GKVAEeHv4fgcVE_gsBtE00Xv742TZWFH4yfjsBPdLpb_mMwFU6BSgZaHVEgLUNUB14B6fjKeunqNE3NA7W-jUbx1Cb8ds3rpb8EjTtOYmVElsV1ZwfWes5HcKhsktfGNjeigwYK_0bFtV45zXmiopBWa3DOETBQhH7g1SXyoKtKtsw0r8Dj8dURMvxrpZ5HaPqIL1AmOzm9paE6jry2ycqJVDI-gHFlwrfykTrXnGaVEu2J0TSIkrkFFuAHm39IYgNMppHn--BhOi7mGtM5gbM1UhhJqJaPj443MlQfJFcpbDmXae7Yxg=w980-h729-no)
