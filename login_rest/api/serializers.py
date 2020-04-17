from rest_framework import serializers
from .models import Persona,Vehiculo

#Creamos una clase que serializa el modelo en Json
class PersonaBasicSerializer(serializers.ModelSerializer):
	class Meta:
		model = Persona
		fields = (
		   'id',
		   'nombre',
		   'apellido',
		   'creado_por',
		)

class VehiculoSerializer(serializers.ModelSerializer):
	class Meta:
		model = Vehiculo
		fields = (
		   'id',
		   'nombre',
		   'modelo',
		   'kilometraje',
		   'personas',
		)

class PersonaSerializer(serializers.ModelSerializer):
	#incluye una lista dentro de otra usando el campo manytomany
	vehiculo_list = VehiculoSerializer(many=True, read_only=True)

	class Meta:
		model = Persona
		fields = (
		   'id',
		   'nombre',
		   'apellido',
		   'creado_por',
		   'vehiculo_list'
		)

