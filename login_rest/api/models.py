from django.db import models

# Create your models here.
class Persona(models.Model):
     id = models.AutoField(primary_key = True)
     nombre = models.CharField('Nombre',max_length=100)
     apellido = models.CharField('Apellido',max_length=50)

     def __str__(self):
          return '{0},{1}'.format(self.apellido,self.nombre)

     class Meta:
          verbose_name = 'Persona'
          verbose_name_plural = 'Personas'