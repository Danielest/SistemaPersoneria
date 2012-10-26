from django.contrib import admin
from docs.models import *


#formulario de Ciudadanos
class CiudadanoAdmin(admin.ModelAdmin):
  #fields = ['nombre', 'apellido1','apellido2','cedula','barrio','direccion','tel','email']
  fieldsets = [
    ('Informacion Personal' , {'fields':['nombre', 'apellido1','apellido2','cedula']}),
    ('Localidad'            , {'fields':['barrio','direccion']}),
    ('Otros'                   , {'fields':['tel','email'],'classes': ['collapse']})
  ]
  list_display = ('nombreCompleto','cedula')
  #list_filter = ['cedula','nombre']
  search_fields = ['cedula','nombre']
  # date_hierarchy = 'pub_date'
admin.site.register(Ciudadano,CiudadanoAdmin)

#formulario de Tutelas
admin.site.register(TipoTutela)

class TutelaAdmin(admin.ModelAdmin):
  fieldset = [
   (None,{'fields': ['accionante','accionado','tipo','fecha_envio','fecha_resp','estado','adjunto']})
   ] 
  list_display   = ('getAccionante','accionado','tipo','fecha_envio','fecha_resp','estado') 
  date_hierarchy = 'fecha_envio'
  search_fields  = ['accionado'] 
  list_filter = ['fecha_envio','fecha_resp']
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

