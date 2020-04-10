from rest_framework import serializers
from .models import Persona

#Creamos una clase que serializa el modelo en Json
class PersonaSerializer(serializers.ModelSerializer):
     class Meta:
          model = Persona
          fields = (
               'id',
               'nombre',
               'apellido'
          )
     
