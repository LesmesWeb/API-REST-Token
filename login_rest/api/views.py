from django.shortcuts import render
from rest_framework import generics
from .models import Persona
from .serializers import PersonaSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

#lista y crea una instancia del modelo 
class PersonaList(generics.ListCreateAPIView):
     queryset  = Persona.objects.all()
     serializer_class = PersonaSerializer
     #permission_classes = (IsAuthenticated,)
     #authentication_class = (TokenAuthentication,)

from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic.edit import FormView
from django.contrib.auth import login, logout,authenticate
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from rest_framework.authtoken.models import Token

class Login(FormView):
     template_name = "login.html"
     form_class = AuthenticationForm
     success_url = reverse_lazy('api:persona_list')

     @method_decorator(csrf_protect) #protección cross site (falsificaciones de solicitudes entre sitios)
     @method_decorator(never_cache) #protección de cache en navegadores
     def dispatch(self,request,*args,**kwargs):
          if request.user.is_authenticated:
               return HttpResponseRedirect(self.get_success_url())
          else:
               return super(Login,self).dispatch(request,*args,*kwargs)

     def form_valid(self,form):
          user = authenticate(username = form.cleaned_data['username'], password = form.cleaned_data['password'])
          token,_ = Token.objects.get_or_create(user = user) #crear el token del usuario
          if token:
               login(self.request, form.get_user())
               return super(Login,self).form_valid(form)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class Logout(APIView):
    def get(self,request, format = None):
        request.user.auth_token.delete()
        logout(request) #cierra la sesión
        return Response(status = status.HTTP_200_OK)
