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
  nombreCompleto.short_description = 'Nombre'


class Documento(models.Model):
 accionante  = models.ForeignKey(Ciudadano)
 accionado   = models.CharField( max_length = 60, default = "" ,help_text="Nombre de la persona con mayuscula Inicial ejemplo * (Juan Carlos, David, Alejandra...)" )
 estado      = models.CharField( max_length = 3, choices = ESTADO, default = "PRO" )
 fecha_envio = models.DateField( blank = False, default = timezone.now() ) 
 fecha_resp  = models.DateField( editable = True , default = timezone.now() + datetime.timedelta(days=16))
 #...
 def __unicode__(self):
  return str(self.id) +" accionada por "+self.accionante.nombre
 
#TUTELAS

class TipoTutela(models.Model):
 nombre = models.CharField(max_length = 20)
 def __unicode__(self):
  return self.nombre


def tutela_filename(instance, filename):
  ext = "."+filename.split(".")[1]
  path = DOCS_FILES+"/tutelas/"
  format =  instance.accionante.cedula + "_" +str(instance.id) + ext
  return os.path.join(path, format)

class Tutela(Documento):
 """corregida"""
 adjunto = models.FileField(upload_to=tutela_filename , blank=True , storage = OverwriteStorage(), help_text="Adjunte archivo")
 tipo    = models.ForeignKey(TipoTutela , help_text="si no encuentra el tipo de tutela haga click en + para agregar uno")
 def __unicode__(self):
  padre = super(Tutela,self).__unicode__()
  return "  "+self.tipo.nombre +" con ID "+ padre
 def tieneAdjunto(self):
  if not self.adjunto:
    return "No"
  else:
    return "Si"  
 tieneAdjunto.short_description = 'Adjunto'

#PETICIOES

class TipoPeticion(models.Model):
 nombre = models.CharField(max_length = 20)
 def __unicode__(self):
  return self.nombre

def peticiones_filename(instance, filename):
  ext = "."+filename.split(".")[1]
  path = DOCS_FILES+"/peticiones/"
  format =  instance.accionante.cedula + "_" +str(instance.id) + ext
  return os.path.join(path, format)

class Peticion(Documento):
 adjunto = models.FileField(upload_to=peticiones_filename , blank=True , storage = OverwriteStorage(), help_text="seleccione la Tutela a gaurdar")
 tipo = models.ForeignKey(TipoPeticion)
 def __unicode__(self):
  padre= super(Peticion,self).__unicode__()
  return padre+" tipo: "+self.tipo.__unicode__()
 def tieneAdjunto(self):
  if not self.adjunto:
    return "No"
  else:
    return "Si"  
 tieneAdjunto.short_description = 'Adjunto'

#DESACATOS

def desacato_filename(instance, filename):
  ext = "."+filename.split(".")[1]
  path = DOCS_FILES+"/desacatos/"
  format =  instance.accionante.cedula + "_" +str(instance.id) + ext
  return os.path.join(path, format)

class Desacato(Documento):
 adjunto = models.FileField(upload_to=desacato_filename , blank=True , storage = OverwriteStorage(), help_text="Archivo de desacato")
 tipo    = models.ForeignKey(TipoTutela , help_text="si no encuentra el tipo de tutela haga click en + para agregar uno")
 radicado = models.CharField(max_length = 30)
 def __unicode__(self):
  return " tipo: "+self.tipo.nombre
 def tieneAdjunto(self):
  if not self.adjunto:
    return "No"
  else:
    return "Si"  
 tieneAdjunto.short_description = 'Adjunto'
#OFICIOS

def oficio_filename(instance, filename):
  ext = "."+filename.split(".")[1]
  path = DOCS_FILES+"/oficios/"+str(instance.id)+"/"
  format =  instance.accionante.cedula + "_" +str(instance.id) + ext
  return os.path.join(path, format)

class Oficio(Documento):
 adjunto      = models.FileField(upload_to=oficio_filename , blank=True , storage = OverwriteStorage(), help_text="Archivo de Oficio")
 asunto       = models.TextField(max_length = 200)
 notificacion = models.TextField(max_length = 200)
 num_fallo    = models.IntegerField()
 @staticmethod
 def autocomplete_search_fields():
  return ("id__iexact", "num_fallo__icontains") 
 def __unicode__(self):
  return "accionado por "+ str(self.accionante.cedula) +" # fallo "+ str(self.num_fallo)
 def tieneAdjunto(self):
  if not self.adjunto:
    return "No"
  else:
    return "Si"  
 tieneAdjunto.short_description = 'Adjunto'

#PROCESOS DICIPLINARIOS

def proceso_filename(instance, filename):
  ext = "."+filename.split(".")[1]
  path = DOCS_FILES+"/oficios/"+str(instance.oficio.id)+"/procesos/"
  format =  instance.get_investigacion_display() + "_" +str(instance.id) + ext
  return os.path.join(path, format)

class ProcesoDisciplinario(models.Model):
 adjunto       = models.FileField(upload_to=proceso_filename , blank=True , storage = OverwriteStorage(), help_text="Seleccione el Archivo del Proceso Diciplinario")
 ent_notific   = models.CharField(max_length = 50,default = "Personeria de manizales" ,verbose_name="Entidad Notificadora",help_text="en este campo se escribe el nombre de la entidad notificadora ")
 estado        = models.CharField( max_length = 3, choices = ESTADO, default = "PRO" )
 fecha_envio   = models.DateField( blank = False, default = timezone.now() )
 fecha_resp    = models.DateField( editable = True, default = timezone.now() + datetime.timedelta(days=16) )
 investigacion = models.CharField( max_length = 4, choices = INVESTIGACIONES )
 oficio        = models.ForeignKey(Oficio)
 def __unicode__(self):
  return self.get_investigacion_display()
 def tieneAdjunto(self):
  if not self.adjunto:
    return "No"
  else:
    return "Si"  
 def getOficio(self):
   return self.oficio.id
 tieneAdjunto.short_description = 'Adjunto' 
 getOficio.short_description = 'Oficio ID' 
 


class Notificacion(models.Model):
  nombre      = models.CharField( max_length = 2, choices = NOTIFICACIONES  )
  descripcion = models.TextField( max_length = 400);
  proc_discip = models.ForeignKey(ProcesoDisciplinario)
  def __unicode__(self):
    return self.get_nombre_display()
#VICTIMAS


class Victima(models.Model):
  accionante  = models.ForeignKey(Ciudadano)
  estado      = models.BooleanField(default = False,help_text="verdadero: aprobado\n falso: pendiente",verbose_name="Aprobado")
  fecha_envio = models.DateField( blank = False, default = timezone.now() ,verbose_name = "Fecha de registro") 
  def __unicode__(self):
    return "accionante: "+self.accionante.__unicode__()+" estado: "+str(self.estado)

def asunto_filename(instance, filename):
  ext = "."+filename.split(".")[1]
  path = DOCS_FILES+"/victimas/"+instance.victima.accionante.cedula+"/asuntos"
  format = str(instance.get_nombre_display()) + ext
  return os.path.join(path, format)

#veo rara la relacion victimas/asunto, o no la entiendo!, pero no la he modificado
class Asunto(models.Model):
  adjunto = models.FileField(upload_to=asunto_filename , blank=True , storage = OverwriteStorage(), help_text="Seleccione el Asunto para la Victima")
  nombre  = models.CharField( max_length = 2, choices=ASUNTOS)
  victima = models.ForeignKey(Victima)
  fecha_envio = models.DateField( blank = False, default = timezone.now() ) 
  def __unicode__(self):
    return "Nombre:  "+self.nombre+" Victima: "+self.victima.__unicode__()
  def tieneAdjunto(self):
   if not self.adjunto:
     return "No"
   else:
     return "Si"  
  tieneAdjunto.short_description = 'Adjunto'

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

