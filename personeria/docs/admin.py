from django.contrib import admin
from docs.models import *


#formulario de Ciudadanos
class CiudadanoAdmin(admin.ModelAdmin):
  #fields = ['nombre', 'apellido1','apellido2','cedula','barrio','direccion','tel','email']
  fieldsets = [
    ('Informacion Personal' , {
      'fields':[('nombre', 'apellido1','apellido2'),'cedula','tel','email']}),#con los parentesis se ponene los campos en la misma fila
    ('Localidad'            , {'fields':['barrio','direccion']})
  ]
  list_display = ('nombreCompleto','cedula')
  search_fields = ['cedula','nombre']
  ordering = ("nombre","apellido1","apellido2","cedula")

admin.site.register(Ciudadano,CiudadanoAdmin)

#formulario de Tutelas
admin.site.register(TipoTutela)

class TutelaAdmin(admin.ModelAdmin):
  fieldset = [
     ("Tutela" , {'fields': ['accionante','accionado','tipo','fecha_envio','fecha_resp','estado','adjunto']})
   ]
  raw_id_fields  = ('accionante',)#esto es para que aparesca un campo de busqueda en vez de un select
  
  list_display   = ('accionante_cedula','accionante_nombre','accionado','tipo','fecha_envio','fecha_resp','estado') 
  date_hierarchy = 'fecha_envio'
  search_fields  = ['accionado','accionante__cedula','accionante__nombre']# para que pueda buscar por llave foranea toca poner modelo__campo
  list_filter = ['estado']
  ordering = ('fecha_envio','fecha_resp')

  def accionante_nombre(self,obj):
    return obj.accionante.nombre
  accionante_nombre.short_description = "Accionante"
  def accionante_cedula(self, obj):
    return obj.accionante.cedula
  accionante_cedula.short_description = "Accionante cedula"

admin.site.register(Tutela,TutelaAdmin)

#formulario de Peticiones
admin.site.register(TipoPeticion)
admin.site.register(Peticion)

#formulario de Desacatos
admin.site.register(Desacato)

#formularios de Oficios
class ProcesoDiciplinarioInline(admin.StackedInline):
 model   = ProcesoDisciplinario
 fk_name = 'oficio'
 extra   = 1

class OficioAdmin(admin.ModelAdmin):
 inlines = [ProcesoDiciplinarioInline]

admin.site.register(Oficio,OficioAdmin)

#formularios de proceso dciplinario
class NotificacionInline(admin.StackedInline):
 model   = Notificacion
 fk_name = 'proc_discip'
 extra   = 1

class ProcesoDiciplinarioAdmin(admin.ModelAdmin):
 inlines = [NotificacionInline]

admin.site.register(ProcesoDisciplinario,ProcesoDiciplinarioAdmin);

#formulario de victimas
class AsuntoInline(admin.TabularInline):
 model = Asunto
 extra = 1

class VictimaAdmin(admin.ModelAdmin):
 inlines = [AsuntoInline]

admin.site.register(Victima,VictimaAdmin);

