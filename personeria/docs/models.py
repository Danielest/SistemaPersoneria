import datetime

from globals import * 
from django.utils import timezone
from django.db import models
from django.forms.extras.widgets import SelectDateWidget
from storage import *

#fecha_respuesta = fecha_envio + termino_contestacion "solo dias habiles"




#database

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
  #aca van los metodos
  def __unicode__(self):
   return (str(self.nombre)+"("+str(self.cedula)+")")
  def related_label(self):
   return (str(self.nombre)+"("+str(self.cedula)+")")
  def nombreCompleto(self):
   return self.nombre+" "+self.apellido1+" "+self.apellido2
  @staticmethod
  def autocomplete_search_fields():
    return ("id__iexact", "nombre__icontains","cedula__icontains")
  #para que se pueda ordenar en el modulo de administracion
  nombreCompleto.admin_order_field = 'nombre'
  nombreCompleto.short_description = 'Nombre Completo'


class Documento(models.Model):
 accionante  = models.ForeignKey(Ciudadano)
 accionado   = models.CharField( max_length = 60, default = "" ,help_text="Nombre de la persona con mayuscula Inicial ejemplo * (Juan Carlos, David, Alejandra...)" )
 estado      = models.CharField( max_length = 3, choices = ESTADO, default = "PRO" )
 fecha_envio = models.DateField( blank = False, default = timezone.now() ) 
 fecha_resp  = models.DateField( editable = True , default = timezone.now() + datetime.timedelta(days=16))
 #...
 def __unicode__(self):
  return "accionante: "+self.accionante.nombre+" accionado: "+self.accionado+" envio: "+str(self.fecha_envio)+" resp: "+str(self.fecha_resp)+" estado: "+self.estado
 
#TUTELAS

class TipoTutela(models.Model):
 nombre = models.CharField(max_length = 20)
 def __unicode__(self):
  return self.nombre


def tutela_filename(instance, filename):
  ext = "."+filename.split(".")[1]
  path = "img/tutela/"
  format =  instance.accionante.cedula + "_" +str(instance.id) + ext
  return os.path.join(path, format)

class Tutela(Documento):
 """corregida"""
 adjunto = models.FileField(upload_to=tutela_filename , blank=True , storage = OverwriteStorage(), help_text="seleccione la Tutela a gaurdar")
 # adjunto = CustomCheckFileField(upload_to="img/tutela", custom_check=_custom_media_file_unique,error_message="File Already Exists",storage=OverwriteStorage())
 tipo    = models.ForeignKey(TipoTutela , help_text="si no encuentra el tipo de tutela haga click en + para agregar uno")
 def __unicode__(self):
  padre = super(Tutela,self).__unicode__()
  return padre+" tipo: "+self.tipo.nombre



#PETICIOES

class TipoPeticion(models.Model):
 nombre = models.CharField(max_length = 20)
 def __unicode__(self):
  return self.nombre

def peticiones_filename(instance, filename):
  ext = "."+filename.split(".")[1]
  path = "img/peticiones/"
  format =  instance.accionante.cedula + "_" +str(instance.id) + ext
  return os.path.join(path, format)

class Peticion(Documento):
 adjunto = models.FileField(upload_to=tutela_filename , blank=True , storage = OverwriteStorage(), help_text="seleccione la Tutela a gaurdar")
 tipo = models.ForeignKey(TipoPeticion)
 def __unicode__(self):
  padre= super(Peticion,self).__unicode__()
  return padre+" tipo: "+self.tipo.__unicode__()

#DESACATOS

class Desacato(Tutela):
 radicado = models.CharField(max_length = 30)
 def __unicode__(self):
  padre = super(Desacato,self).__unicode__()
  return padre+" radicado: "+self.radicado

#OFICIOS

class Oficio(Documento):
 adjunto      = models.FileField(upload_to = 'img/oficios')
 asunto       = models.TextField(max_length = 200)
 notificacion = models.TextField(max_length = 200)
 num_fallo    = models.IntegerField()
 def __unicode__(self):
  padre = super(Oficio,self).__unicode__()
  return (padre+" \n Asunto: "+self.asunto+
         "\n notificacion: "+self.notificacion+" proceso diciplinario: ")

#PROCESOS DICIPLINARIOS

class ProcesoDisciplinario(models.Model):
 adjunto       = models.FileField(upload_to = 'img/procesos_diciplinarios')
 ent_notific   = models.TextField(max_length = 200)
 estado        = models.CharField( max_length = 3, choices = ESTADO, default = "PRO" )
 fecha_envio   = models.DateField( blank = False, default = timezone.now() )
 fecha_resp    = models.DateField( editable = True, default = timezone.now() + datetime.timedelta(days=16) )
 investigacion = models.CharField( max_length = 2, choices = INVESTIGACIONES )
 oficio        = models.ForeignKey(Oficio)
 def __unicode__(self):
  return " investigacion: "+self.investigacion

class Notificacion(models.Model):
  nombre      = models.CharField( max_length = 2, choices = NOTIFICACIONES  )
  descripcion = models.CharField( max_length = 400);
  proc_discip = models.ForeignKey(ProcesoDisciplinario)
  def __unicode__(self):
    return "Nombre: "+self.nombre+" Proceso Disciplinario: "+self.proc_discip.__unicode__()

#VICTIMAS


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

