from rest_framework import serializers
from .models import Persona,Vehiculo,Group,User

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
	personas = PersonaBasicSerializer(many=True)
	class Meta:
		model = Vehiculo
		fields = (
		   'id',
		   'nombre',
		   'modelo',
		   'kilometraje',
		   'personas',
		)


class VehiculoBasicSerializer(serializers.ModelSerializer):
	class Meta:
		model = Vehiculo
		fields = (
		   'id',
		   'nombre',
		   'modelo',
		   'kilometraje',
		)

class PersonaSerializer(serializers.ModelSerializer):
	#incluye una lista dentro de otra usando el campo manytomany
	vehiculo_list = VehiculoBasicSerializer(many=True, read_only=True)

	class Meta:
		model = Persona
		fields = (
		   'id',
		   'nombre',
		   'apellido',
		   'creado_por',
		   'vehiculo_list'
		)


from django.utils.timezone import now

class GroupSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Group
        fields = ('name',)

#Obtención de grupos de usuarios
class UserSerializers(serializers.ModelSerializer):
	# Apoyado de: https://www.django-rest-framework.org/api-guide/fields/#serializermethodfield
	days_since_joined = serializers.SerializerMethodField()
	groups = GroupSerializer(many=True)
	#extra_kwargs = {'password': {'write_only': False}}
	class Meta:
		model = User
		fields = ('id', 'username','email','is_active', 
			  'is_superuser', 'date_joined', 'groups','days_since_joined')

	def get_days_since_joined(self, obj):
		return (now() - obj.date_joined).days

