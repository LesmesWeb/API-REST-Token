# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User,Group

# Create your models here.
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