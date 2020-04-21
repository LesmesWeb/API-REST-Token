from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Persona,Vehiculo
from .serializers import PersonaBasicSerializer,PersonaSerializer,VehiculoSerializer,UserSerializers

#IsAuthenticated: clase de permiso denegará el permiso a cualquier usuario no autenticado 
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

"""
generics: acceso directo para patrones de usos comunes para que pueda 
escribir rápidamente.
ListCreateAPIView: listar y crear una instancia del modelo para 
lectura y escritura (get y post) 
"""

from rest_framework import generics

class PersonaList(generics.ListCreateAPIView):
	queryset  = Persona.objects.all()
	serializer_class = PersonaBasicSerializer
	permission_classes = (IsAuthenticated,)
	authentication_class = (TokenAuthentication,)

from rest_framework import viewsets

"""
viewsets: es simplemente un tipo de Vista basada en clases, 
que no proporciona ningún manejador de métodos como .get()o .post(), 
y en su lugar proporciona acciones como .list()y .create()
ReadOnlyModelViewSetclase: Proporciona solo acciones de lectura
"""

class PersonaViewSet(viewsets.ReadOnlyModelViewSet):
	queryset  = Persona.objects.all()
	serializer_class = PersonaSerializer
	permission_classes = (IsAuthenticated,)
	authentication_class = (TokenAuthentication,)

class VehiculoViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = Vehiculo.objects.all()
	serializer_class = VehiculoSerializer
	permission_classes = (IsAuthenticated,)
	authentication_class = (TokenAuthentication,)


class UserGroupViewSet(viewsets.ReadOnlyModelViewSet):
	queryset  = User.objects.all()
	serializer_class = UserSerializers
	permission_classes = (IsAuthenticated,)
	authentication_class = (TokenAuthentication,)

"""
Usamos las siguientes librerias para armar nuestro propio
formulario de inicio de sesión con protecciónes por medio
de decoradores y que a su generar el token.
"""

from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic.edit import FormView
from django.contrib.auth import login, logout,authenticate
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from rest_framework.authtoken.models import Token

"""
DRF agrega sufijos en los conjuntos de vistas para diferentes URL con
apoyo de basename: ejemplo:
 	success_url = reverse_lazy('api:api_vehiculo-list')
 	success_url = reverse_lazy('api:api_vehiculo-detail')
"""

class Login(FormView):
	template_name = "login.html"
	form_class = AuthenticationForm
	success_url = reverse_lazy('api:api_vehiculo-list')

	#protección cross site (falsificaciones de solicitudes entre sitios)
	@method_decorator(csrf_protect)
	#protección de cache en navegadores 
	@method_decorator(never_cache) 

	#dispatch: es un metodo HTTP que toma y envia una solicitud
	def dispatch(self,request,*args,**kwargs):
		if request.user.is_authenticated:
			return HttpResponseRedirect(self.get_success_url())
		else:
			return super(Login,self).dispatch(request,*args,*kwargs)

	#form_valid: este metodo es habilitado cuando los datos del formulario son validos y devuelve un HttpResponse
	def form_valid(self,form):
		user = authenticate(username = form.cleaned_data['username'], password = form.cleaned_data['password'])
		
		#crear el token del usuario
		token,_ = Token.objects.get_or_create(user = user)
		if token:
			login(self.request, form.get_user())
			return super(Login,self).form_valid(form)

"""
APIView: Permite utilizar vista basadas en clases y reutilizar funcionalidades
comunes como: get_object, get,put,put, delete y post
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status #Codigo de respuesta

class Logout(APIView):
	def get(self,request, format = None):
		request.user.auth_token.delete() #Elimina el registro del token
		logout(request) 				 #cierra la sesión
		return Response(status = status.HTTP_200_OK)