from django.shortcuts import render
from rest_framework import generics
from .models import Persona
from .serializers import PersonaSerializer

#lista y crea una instancia del modelo 
class PersonaList(generics.ListCreateAPIView):
     queryset  = Persona.objects.all()
     serializer_class = PersonaSerializer
