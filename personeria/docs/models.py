import datetime
from django.db import models

# Create your models here.

INVESTIGACIONES = (
 ('IP','investigacion preliminar'),
 ('ID','investigacion disciplinaria'),
 ('IP','investigacion de pruebas'),
 ('TC','translado de conclusion'),
)

#fecha_respuesta = fecha_envio + termino_contestacion "solo dias habiles"

TERMINO_DE_COTESTACION = 16
TERMINO_DE_COTESTACION_OFICIOS = 10
TERMINO_DE_COTESTACION_PROCESOS_DICOPLINARIOS = 3  


class Ciudadanos(models.Model):
 nombre    = models.CharField(max_length = 20)
 apellido1 = models.CharField('primer apellido', max_length = 20)
 apellido2 = models.CharField('segundo apellido', max_length = 20)
 cedula    = models.CharField(max_length = 25) 
 direccion = models.CharField(max_length = 100)
 barrio    = models.CharField(max_length = 30)
 tel       = models.IntegerField('telefono', max_length = 15)
 email     = models.EmailField(max_length = 30)
 #...
 def __unicode__(self):
  return "nombre:",self.nombre,self.apellido1,self,apellido2," cedula:",self.cedula," direccion:",self.direccion," barrio:",self.barrio," tel:",self.tel," email:",self.email
 def nombreCompleto(self):
  return self.nombre,self.apellido1,self.apellido2

class Documentos(models.Model):
 accionante   = models.ForeignKey(Ciudadanos)
 accionado   = models.CharField(max_length = 60)
 fecha_envio = models.DateField('fecha de envio', blank = False, null = False)
 fecha_resp  = models.DateField('fecha de respuesta', blank = False, null = False)
 estado      = models.BooleanField()
 adjunto     = models.FileField(max_length = 300, upload_to = 'docs')
 #...
 def __unicode__(self):
  return "accionante:",self.accionante," accionado:",self.accionado," envio:",self.fecha_envio," resp:",self.fecha_resp," estado:",self.estado

class TiposDeTutelas(models.Model):
 nombre = models.CharField(max_length = 20)
 def __unicode__(self):
  return "nombre: ",self.nombre
  

class Tutelas(Documentos):
 tipo = models.ForeignKey(TiposDeTutelas)
 def __unicode__(self):
  return "tipo:",self.tipo

class TipoPeticiones(models.Model):
 nombre = models.CharField(max_length = 20)
 def __unicode__(self):
  return "nombre:",self.nombre

class Peticiones(Documentos):
 tipo = models.ForeignKey(TipoPeticiones)
 def __unicode__(self):
  return "tipo:",self.tipo

class Desacatos(Tutelas):
 radicado = models.CharField(max_length = 30)
 def __unicode__(self):
  return "radicado:",self.radicado

class ProcesosDiciplinarios(Documentos):
 investigacion = models.CharField(max_length = 2, choices = INVESTIGACIONES)
 def __unicode__(self):
  return "investigacion:",self.investigacion

class Oficios(Documentos):
 asutno            = models.TextField(max_length = 200)
 term_de_cont      = models.TextField('termino de contestacion', max_length = 200)
 notificacion      = models.TextField(max_length = 200)
 proceso_diciplinario = models.ForeignKey(ProcesosDiciplinarios)
 def __unicode__(self):
  return "asuto:",self.asutno," termino de contestacion:",self.term_de_cont," notificacion:",self.notificacion," proceso diciplinario:",self.proceso_diciplinario

        

