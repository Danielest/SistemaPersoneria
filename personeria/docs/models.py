import datetime
from globals import *
from django.utils import timezone
from django.db import models
# from django.contrib.auth.models import User, Groups

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
  return ("nombre: "+self.nombre+" "+self.apellido1+" "+self.apellido2+
        " cedula: "+self.cedula+" direccion: "+self.direccion+" barrio: "+self.barrio+
        " tel: "+self.tel+" email: "+self.email)
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
  return "nombre: "+self.nombre

class Peticiones(Documentos):
 tipo = models.ForeignKey(TipoPeticiones)
 def __unicode__(self):
  padre= super(Peticiones,self).__unicode__()
  return padre+" tipo: "+self.tipo.__unicode__()

class Desacatos(Tutelas):
 radicado = models.CharField(max_length = 30)
 def __unicode__(self):
  padre = super(Desacatos,self).__unicode__()
  return padre+" radicado: "+self.radicado

class Investigacion(models.Model):
  nombre = models.CharField( max_length = 2, choices = INVESTIGACIONES )
  def __unicode__(self):
    return "Nombre: "+self.nombre


class Oficios(Documentos):
 asunto            = models.TextField(max_length = 200)
 term_de_cont      = models.TextField('termino de contestacion', max_length = 200)
 notificacion      = models.TextField(max_length = 200)
 def __unicode__(self):
  padre = super(Oficios,self).__unicode__()
  return (padre+" asunto: "+self.asunto+" termino de contestacion: "+self.term_de_cont+
         " notificacion: "+self.notificacion+" proceso diciplinario: "+self.proceso_diciplinario.__unicode__())

class ProcesosDisciplinarios(Documentos):
 investigacion = models.ForeignKey(Investigacion)#hice esta modificacion porque aqui va la foranea de investigacion
 oficio        = models.ForeignKey(Oficios)
 def __unicode__(self):
  padre = super(ProcesosDisciplinarios,self).__unicode__()
  return padre+" investigacion: "+self.investigacion.__unicode__()


class Notificacion(models.Model):
  nombre                = models.CharField( max_length = 2, choices = NOTIFICACIONES  )
  proceso_disciplinario = models.ForeignKey(ProcesosDisciplinarios)
  def __unicode__(self):
    return "Nombre: "+self.nombre+" Proceso Disciplinario: "+self.proceso_disciplinario.__unicode__()


class Victimas(models.Model):
  accionante = models.ForeignKey(Ciudadanos)
  estado     = models.BooleanField(default = False, blank= False)
  def __unicode__(self):
    return "accionante: ",self.accionante.__unicode__," estado: ", self.estado

#veo rara la relacion victimas/asunto, o no la entiendo!, pero no la he modificado
class Asunto(models.Model):
  #adjunto = models.FileField(max_length = 30, upload_to = 'asuntos')
  nombre  = models.CharField( max_length = 2, choices=ASUNTOS)
  victima = models.ForeignKey(Victimas)
  def __unicode__(self):
    return "Nombre:  "+self.nombre+" Victima: "+self.victima.__unicode__()

# class Funcionario(models.Model):
#   apellido1 = models.CharField( max_length = 45, default= "" )
#   apellido2 = models.CharField( max_length = 45, blank = True, default = "" )
#   cedula = models.CharField( max_length = 15, default = "" )
#   direccion = models.CharField( max_length = 15, default = "" )
#   nombre = models.CharField( max_length = 45, default="" )
#   barrio = models.CharField( max_length = 45, default="" )
#   tel = models.CharField( max_length = 20, blank = True, default = "" )
#   email = models.EmailField( max_length = 30,blank = True, default = "" )
#   adjunto = models.FileField(max_length = 30, upload_to = 'funcionarios')
#   user= models.ForeignKey(User)
#   rol = models.ForeignKey(Rol)
#   def __unicode__(self):
#    return "nombre: "+self.nombre+" "+self.apellido1+" "+self.apellido2+" cedula: "+self.cedula+" direccion: "+self.direccion+" barrio: "+self.barrio+" tel: "+self.tel+" email: "+self.email+" User: "+self.user.nick

