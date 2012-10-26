import datetime
from globals import *
from django.utils import timezone
from django.db import models
# from django.contrib.auth.models import User, Groups

#fecha_respuesta = fecha_envio + termino_contestacion "solo dias habiles"


class TerminoDeContestacion(models.Model):
 """esta tabla brinda para cada documento el numero de dias que se tendra para el calculo de la fecha de respuesta"""
 nombre = models.CharField( max_length = 3 ,choices = TERMINO_DE_COTESTACION)
 dias   = models.IntegerField()


class Ciudadano(models.Model):
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
 #para que se pueda ordenar en el modulo de administracion
 nombreCompleto.admin_order_field = 'nombre'
 nombreCompleto.short_description = 'Nombre Completo'



class Documento(models.Model):
 accionante  = models.ForeignKey(Ciudadano)
 accionado   = models.CharField( max_length = 60, default = "" )
 estado      = models.CharField( max_length = 3, choices = ESTADO, default = "PRO" )
 fecha_envio = models.DateField( blank = False, default = timezone.now() )
 fecha_resp  = models.DateField( editable = True )
 #...
 def __unicode__(self):
  return "accionante: "+self.accionante.nombre+" accionado: "+self.accionado+" envio: "+str(self.fecha_envio)+" resp: "+str(self.fecha_resp)+" estado: "+self.estado

class TipoTutela(models.Model):
 nombre = models.CharField(max_length = 20)
 def __unicode__(self):
  return "nombre: "+self.nombre

class Tutela(Documento):
 """corregida"""
 adjunto = models.FileField(upload_to = 'img/tutelas')
 tipo    = models.ForeignKey(TipoTutela)
 def __unicode__(self):
  padre = super(Tutela,self).__unicode__()
  return padre+" tipo: "+self.tipo.nombre
 def getAccionante(self):
    return self.accionante.cedula
 getAccionante.short_description = "Accionante"

class TipoPeticion(models.Model):
 nombre = models.CharField(max_length = 20)
 def __unicode__(self):
  return "nombre: "+self.nombre

class Peticion(Documento):
 adjunto = models.FileField(upload_to = 'img/peticiones')
 tipo = models.ForeignKey(TipoPeticion)
 def __unicode__(self):
  padre= super(Peticiones,self).__unicode__()
  return padre+" tipo: "+self.tipo.__unicode__()

class Desacato(Tutela):
 radicado = models.CharField(max_length = 30)
 def __unicode__(self):
  padre = super(Desacato,self).__unicode__()
  return padre+" radicado: "+self.radicado

#
#
# DESDE ACA FALTA SEGUIR PARA COMPLETAR EL MODELO
#
#

class Oficio(Documento):
 adjunto      = models.FileField(upload_to = 'img/oficios')
 asunto       = models.TextField(max_length = 200)
 notificacion = models.TextField(max_length = 200)
 num_fallo    = models.IntegerField()
 def __unicode__(self):
  padre = super(Oficio,self).__unicode__()
  return (padre+" \n Asunto: "+self.asunto+
         "\n notificacion: "+self.notificacion+" proceso diciplinario: ")

class ProcesoDisciplinario(models.Model):
 adjunto       = models.FileField(upload_to = 'img/procesos_diciplinarios')
 ent_notific   = models.TextField(max_length = 200)
 estado        = models.CharField( max_length = 3, choices = ESTADO, default = "PRO" )
 fecha_envio   = models.DateField( blank = False, default = timezone.now() )
 fecha_resp    = models.DateField( editable = True ) 
 investigacion = models.CharField( max_length = 2, choices = INVESTIGACIONES )
 oficio        = models.ForeignKey(Oficio)
 def __unicode__(self):
<<<<<<< HEAD
  return " investigacion: "+self.investigacion
=======
  padre = super(ProcesosDisciplinarios,self).__unicode__()
  return padre+" investigacion: "+self.investigacion.__unicode__()

>>>>>>> b34de2e4c3eec119904758814684de968d5375d2

class Notificacion(models.Model):
  nombre      = models.CharField( max_length = 2, choices = NOTIFICACIONES  )
  descripcion = models.CharField( max_length = 400);
  proc_discip = models.ForeignKey(ProcesoDisciplinario)
  def __unicode__(self):
    return "Nombre: "+self.nombre+" Proceso Disciplinario: "+self.proc_discip.__unicode__()


class Victima(models.Model):
  accionante = models.ForeignKey(Ciudadano)
  estado     = models.BooleanField(default = False)
  def __unicode__(self):
    return "accionante: "+self.accionante.__unicode__()+" estado: "+str(self.estado)

#veo rara la relacion victimas/asunto, o no la entiendo!, pero no la he modificado
class Asunto(models.Model):
  adjunto = models.FileField(upload_to = 'asuntos')
  nombre  = models.CharField( max_length = 2, choices=ASUNTOS)
  victima = models.ForeignKey(Victima)
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

