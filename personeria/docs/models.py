from django.db import models

# Create your models here.

INVESTIGACIONES = (
 ('IP','investigacion preliminar'),
 ('ID','investigacion disciplinaria'),
 ('IP','investigacion de pruebas'),
 ('TC','translado de conclusion'),
)

class Ciudadanos(models.Model):
 nombre    = models.CharField(max_length = 20)
 apellido1 = models.CharField('primer apellido', max_length = 20)
 apellido2 = models.CharField('segundo apellido', max_length = 20)
 cedula    = models.CharField(max_length = 25) 
 direccion = models.CharField(max_length = 100)
 barrio    = models.CharField(max_length = 30)
 tel       = models.IntegerField('telefono', max_length = 15)
 email     = models.EmailField(max_length = 30)
 

class Documentos(models.Model):
 accinante   = models.ForeignKey(Ciudadanos)
 accionado   = models.CharField(max_length = 60)
 fecha_envio = models.DateField('fecha de envio', blank = False, null = False)
 fecha_resp  = models.DateField('fecha de respuesta', blank = False, null = False)
 estado      = models.BooleanField()
 adjunto     = models.FileField(max_length = 300, upload_to = 'docs')

class TiposDeTutelas(models.Model):
 nombre = models.CharField(max_length = 20)

class Tutelas(Documentos):
 tipo = models.ForeignKey(TiposDeTutelas)

class TipoPeticiones(models.Model):
 nombre = models.CharField(max_length = 20)
 
class Peticiones(Documentos):
 tipo = models.ForeignKey(TipoPeticiones)

class Desacatos(Tutelas):
 radicado = models.CharField(max_length = 30)

class ProcesosDiciplinarios(Documentos):
 investigacion = models.CharField(max_length = 2, choices = INVESTIGACIONES)

class Oficios(Documentos):
 asutno            = models.TextField(max_length = 200)
 term_de_cont      = models.TextField('termino de contestacion', max_length = 200)
 notificacion      = models.TextField(max_length = 200)
 proc_diciplinario = models.ForeignKey(ProcesosDiciplinarios)
 

        

