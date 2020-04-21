
# API Rest Vehículos - PowerBI

Este proyecto esta basado en la documentación de Django Rest con apoyo en el uso de autenticación REST del tutorial de [Developer.pe](https://www.youtube.com/watch?v=kh4YFQrvVyE&list=PLMbRqrU_kvbRzgD2s7JHvJxGs6FdvFjg9&index=6) , este es un proyecto de aprendizaje personal, el cual esta abierto para recibir sugerencias y si es posible añadir nuevos elementos.

Actualmente cuenta con una base de datos en PostgreSQL que contiene las siguientes tablas:

![MER ACTUAL](https://raw.githubusercontent.com/Dev-Lesmes/API-REST-Token/master/img_documentacion/MER_ALL_MODELS.png)

## DEMO  POWERBI v1.1
[https://app.powerbi.com/view?r=eyJrIjoiZDMwN2E2OTUtZDc4OC00OTMxLTgxZTgtMzQ3MGYyNTRmNTVkIiwidCI6IjVlNmY0NzE0LTk4YmQtNGRhMS1hOGY1LTNjYTQ1OWVhYmRjOSIsImMiOjR9](https://app.powerbi.com/view?r=eyJrIjoiZDMwN2E2OTUtZDc4OC00OTMxLTgxZTgtMzQ3MGYyNTRmNTVkIiwidCI6IjVlNmY0NzE0LTk4YmQtNGRhMS1hOGY1LTNjYTQ1OWVhYmRjOSIsImMiOjR9)

Cuenta con los siguiente elementos:

 - **CORS:** para conexiones desde otros equipos (aclarar que para que funcione se debe correr de la siguiente manera: python3 manage.py runserver 0.0.0.0 y se llama con la IP local del equipo.
 - **Documentación:**  cuenta con el apartado de la documentación ya implementado usando la librerías como: **swagger** y **coreapi**.
 - **Token:** Autenticación por Token y cierre de sesión
 - **Serializers:** en el que podemos obtener la lista y detalle de los vehículos con sus personas, de la misma manera las personas que tienen los vehiculos (manytomany). Por ultimo se genero una lista usuarios con su lista de grupos.
 - **PowerBI:** Se desarrollo una plantilla que consume los datos del API para generar gráficas para asegurarnos que el consumo del API rest fue el correcto

-- Desde este punto se incluye los pasos relevantes del proyecto, al igual en los **commits** puede visualizar lo que se ha ido realizando.

## Ejecución del Proyecto

```sh
$source rest_env/bin/activate           #Activar entorno
$cd ..                                  #regresar
$pip3 install -r requirements.txt       #Instalar paquetes pip3
$cd /login_rest                         #ingresar a la carpeta del proyecto
$python3 manage.py runserver 0.0.0.0:8001 #ejecutar proyecto con puerto abiertos
```
## Tips:
Si se desea visualizar los modelos de la base de datos gráficas mente tipo **MER** (modelo entidad relacion) hacer lo siguiente:
```sh 
--instalar los siguientes paquetes y libreria
$ sudo apt-get install graphviz libgraphviz-dev pkg-config  
$ pip install pygraphviz #interfaz de Python para los gráficos
$ pip install django-extensions 

-- Añadir en el settings.py la siguiente app:

INSTALLED_APPS = [  
    ...
    'django_extensions', 
]
```
Para crear el gráfico se debe iniciar el siguiente comando al interior del proyecto:
```sh 
-- Genera un grafico del app seleccionada (api)
$ python manage.py graph_models api -o APP_MODELS.png

-- Genera grafico de todos los modelos incluyendo los que vienen por defecto de Django
$ python3 manage.py graph_models --pygraphviz -a -g -o MER_ALL_MODELS.png
```

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
 'django_extensions' #usamos esta libreria para generar el MER
]

TIME_ZONE = 'CO'  # America/Bogota (https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)
```

-- app/models.py

```sh
class Persona(models.Model):
    id = models.AutoField(primary_key = True)
    nombre = models.CharField('Nombre',max_length=100)
    apellido = models.CharField('Apellido',max_length=50)
    creado_por = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
      return '{0},{1}'.format(self.apellido,self.nombre)

    class Meta:
      verbose_name = 'Persona'
      verbose_name_plural = 'Personas'

class Vehiculo(models.Model):
    id = models.AutoField(primary_key = True)
    nombre = models.CharField('Nombre',max_length=100)
    modelo = models.CharField('Modelo',max_length=50)
    kilometraje = models.IntegerField('Kilometraje',default=0,null=True,blank=False)
    personas = models.ManyToManyField(Persona,related_name="vehiculo_list", blank=True)

    def __str__(self):
          return 'Modelo: {0}, Kilometraje: {1}'.format(self.modelo,self.kilometraje)

    class Meta:
        verbose_name = 'Vehiculo'
        verbose_name_plural = 'Vehiculos'
        ordering = ['kilometraje']
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

![Postman validación token ](https://raw.githubusercontent.com/Dev-Lesmes/API-REST-Token/master/img_documentacion/testing_rest/api_generate_token.png)

Otra herramienta para realizar la validación es **httpie**para validar por se requiere instalar.
-- pip3 install httpie
-- Para ejecutar por POST con esa libreria y general token se hace de la siguiente manera:

```sh
http http://localhost:8001/api_generate_token/ username="admin" password="admin123"
```

![httpie validación](https://raw.githubusercontent.com/Dev-Lesmes/API-REST-Token/master/img_documentacion/testing_rest/2.htttpie_token.png)

<hr>

### Token en lista de personas

Es necesario que ahora nuestra lista de persona en la url [http://localhost:8000/api/1.0/persona/](http://localhost:8001/api/1.1/personas/) permite la autenticación buscando el token automáticamente.

De la manera manual seria de esta manera con **httpie**:

```sh
http http://localhost:8001/api/1.1/personas/ "Authorization: Basic YWRtaW46YWRtaW4xMjM="
```
Actualmente para que la conecciión se exito con **PowerBI** se quiere que el parametro de acceso sea con **Authorization basic** de la siguiente manera:

![postman validación lista de personas](https://raw.githubusercontent.com/Dev-Lesmes/API-REST-Token/master/img_documentacion/testing_rest/3.postman_lista_personas.png)

## Login y Logout Token authentication

Se diseñara un login que guarde el Token del usuario que inicie sesión y se cambiara el permiso directamente en la clase, además se incluirá la opción de cerrar sesión y que se elimine el Token:

 1. Crear un template templates/login.html
 2. Crear dos clases que permita la creación del usuario con su Token y cerrar sesión con la eliminación del Token en api/views.py 
 3. Llamar las clases para iniciar y cerrar sesión login_rest/url.py

## Opciones para documentar API

-- Habilitar en el settings.py las schamas

```sh

REST_FRAMEWORK = { 
        'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema'
    }

```

- Instalar las siguientes librerias
-- coreapi
-- django-rest-swagger

- Añadir las rutas de la documentación:

```sh
from rest_framework.documentation import include_docs_urls
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='api')

urlpatterns = [
    ...
    path('docs/', include_docs_urls(title='api')),
    path(r'swagger-docs/', schema_view),
]
```
## Añadir Cors

- Instalar lo siguiente:
-- pip install django-cors-headers

--Configurar el setting.py

```sh

CORS_ORIGIN_ALLOW_ALL=True

INSTALLED_APPS = [
    ...
    'corsheaders',
    ...
]


MIDDLEWARE_CLASSES = [
    ...
    'corsheaders.middleware.CorsMiddleware',
    ...
    'django.middleware.csrf.CsrfViewMiddleware',
    'corsheaders.middleware.CorsPostCsrfMiddleware',
    ...
]
```
## PowerBI

Para realizar la conexión como anteriormente se menciono es importante que se tenga el CORS activo, que la autenticación sea basic y que la estructura del json se comporte de la siguiente manera:

```sh
[
    {
        "id": 1,
        "nombre": "Kia",
        "modelo": "RIO2020",
        "kilometraje": 0,
        "personas": [
            {
                "id": 1,
                "nombre": "Dev",
                "apellido": "Lesmes",
                "creado_por": 1
            },
            {
                "id": 2,
                "nombre": "Nombre",
                "apellido": "Apellido",
                "creado_por": 1
            }
        ]
]
```
1. La conexión se hace de esta forma web en la que se envia el valor el autentication basic, con la ip del equipo en el que se encuentra el API:
![1.Conexion_con_Autorizacion_PowerBI](https://raw.githubusercontent.com/Dev-Lesmes/API-REST-Token/master/img_documentacion/powerbi/1.Conexion_con_Autorizacion_PowerBI.png)

2. En la edición de consultas para pasar parámetros de manera dinámica:
![1.Conexion_con_Autorizacion_PowerBI](https://raw.githubusercontent.com/Dev-Lesmes/API-REST-Token/master/img_documentacion/powerbi/2.JSON_a_Tabla_PowerBI.png)

3.  Se deben expandir los datos y seleccionar las columnas para poder acceder a los submodulos:
![1.Conexion_con_Autorizacion_PowerBI](https://raw.githubusercontent.com/Dev-Lesmes/API-REST-Token/master/img_documentacion/powerbi/3.Expandir_listar_internas_PowerBI.png)

4. PowerBi por defecto genera unas relaciones pero no son las mas apropiadas así que hay que indicarle como sera su relación y quedaría de la siguiente manera:
![1.Conexion_con_Autorizacion_PowerBI](https://raw.githubusercontent.com/Dev-Lesmes/API-REST-Token/master/img_documentacion/powerbi/5.Relaciones_PowerBI)


5. Este es el resultado 
![1.Conexion_con_Autorizacion_PowerBI](https://raw.githubusercontent.com/Dev-Lesmes/API-REST-Token/master/img_documentacion/powerbi/4.Grafica_PowerBI.png)