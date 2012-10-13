import datetime
from globals import *
from django.utils import timezone
from django.db import models


# Create your models here.

INVESTIGACIONES = (
 ('IP','investigacion preliminar'),
 ('ID','investigacion disciplinaria'),
 ('IP','investigacion de pruebas'),
 ('TC','translado de conclusion'),
)


#fecha_respuesta = fecha_envio + termino_contestacion "solo dias habiles"


class TerminoDeContestacion(models.Model):
 """maneja el termino de contestacion"""
 nombre = models.CharField( max_length = 3 ,choices = TERMINO_DE_COTESTACION)
 dias   = models.IntegerField()

        
class Ciudadanos(models.Model):
 apellido1 = models.CharField( max_length = 20, default = "" )
 apellido2 = models.CharField( max_length = 20, blank = True, default = "" )
 barrio    = models.CharField( max_length = 30, default = "" )
 cedula    = models.CharField( max_length = 25, default = "" ) 
 direccion = models.CharField( max_length = 100, default = "" )
 email     = models.EmailField( max_length = 30,blank = True, default = "" )
 nombre    = models.CharField( max_length = 20, default = "" )
 tel       = models.CharField( max_length = 15, blank = True, default = "" ) 
 #...
 def __unicode__(self):
  return "nombre: "+self.nombre+" "+self.apellido1+" "+self.apellido2+" cedula: "+self.cedula+" direccion: "+self.direccion+" barrio: "+self.barrio+" tel: "+self.tel+" email: "+self.email
 def nombreCompleto(self):
  return self.nombre+" "+self.apellido1+" "+self.apellido2
 
class Documentos(models.Model):
 accionante  = models.ForeignKey(Ciudadanos)
 accionado   = models.CharField( max_length = 60, default = "" )
 estado      = models.CharField( max_length = 3, choices = ESTADO, default = "PRO" )
 fecha_envio = models.DateField( blank = False, default = timezone.now() )
 fecha_resp  = models.DateField( editable = False , null=True)
 #...
 def __unicode__(self):
  return "accionante: "+self.accionante.nombre+" accionado: "+self.accionado+" envio: "+str(self.fecha_envio)+" resp: "+str(self.fecha_resp)+" estado: "+self.estado

class TiposDeTutelas(models.Model):
 nombre = models.CharField(max_length = 20)
 def __unicode__(self):
  return "nombre: "+self.nombre
  

class Tutelas(Documentos):
 """corregida""" 
 tipo    = models.ForeignKey(TiposDeTutelas)
 adjunto = models.FileField(max_length = 30, upload_to = 'tutelas')
 def __unicode__(self):
  padre = super(Tutelas,self).__unicode__()  
  return padre+" tipo: "+self.tipo.nombre


#
#
# DESDE ACA FALTA SEGUIR PARA COMPLETAR EL MODELO
#
#

class TipoPeticiones(models.Model):
 nombre = models.CharField(max_length = 20)
 def __unicode__(self):
  return "nombre: ",self.nombre

class Peticiones(Documentos):
 tipo = models.ForeignKey(TipoPeticiones)
 def __unicode__(self):
  return "tipo: ",self.tipo

class Desacatos(Tutelas):
 radicado = models.CharField(max_length = 30)
 def __unicode__(self):
  return "radicado: ",self.radicado

class ProcesosDiciplinarios(Documentos):
 investigacion = models.CharField(max_length = 2, choices = INVESTIGACIONES)
 def __unicode__(self):
  return "investigacion: ",self.investigacion

class Oficios(Documentos):
 asutno            = models.TextField(max_length = 200)
 term_de_cont      = models.TextField('termino de contestacion', max_length = 200)
 notificacion      = models.TextField(max_length = 200)
 proceso_diciplinario = models.ForeignKey(ProcesosDiciplinarios)
 def __unicode__(self):
  return "asuto: ",self.asutno," termino de contestacion: ",self.term_de_cont," notificacion: ",self.notificacion," proceso diciplinario: ",self.proceso_diciplinario

        

