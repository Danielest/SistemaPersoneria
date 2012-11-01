from django.contrib import admin
from docs.models import *


class CiudadanoAdmin(admin.ModelAdmin):
  fieldsets = [
    ('Informacion Personal' , {
      'fields':[('nombre', 'apellido1','apellido2'),'cedula','tel','email']}),#con los parentesis se ponene los campos en la misma fila
    ('Localidad'            , {'fields':['barrio','direccion']})
  ]
  list_display = ('nombreCompleto','cedula')
  search_fields = ['cedula','nombre']
  ordering = ("nombre","apellido1","apellido2","cedula")

class TutelaAdmin(admin.ModelAdmin):
  fieldset = [
     ("Tutela" , {'fields': ['accionante','accionado','tipo','fecha_envio','fecha_resp','estado','adjunto']})
   ]
  raw_id_fields  = ('accionante',)#esto es para que aparezca un campo de busqueda en vez de un select

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

class ProcesoDiciplinarioInline(admin.StackedInline):
  """Formulario de oficios"""
  model   = ProcesoDisciplinario
  fk_name = 'oficio'
  extra   = 1

class DesacatoAdmin(admin.ModelAdmin):
  fieldsets = [
      ("Desacato" , {'fields': ['accionante','accionado','tipo','fecha_envio','fecha_resp','estado','adjunto']})#con los parentesis se ponene los campos en la misma fila
  ]
  raw_id_fields  = ('accionante',)
  list_display   = ('accionante_cedula','accionante_nombre','accionado','tipo','fecha_envio','fecha_resp','estado')
  list_filter = ['estado']
  search_fields  = ['accionado','accionante__cedula','accionante__nombre']
  date_hierarchy = 'fecha_envio'
  def accionante_nombre(self,obj):
     return obj.accionante.nombre
  accionante_nombre.short_description = "Accionante"
  def accionante_cedula(self, obj):
     return obj.accionante.cedula
  accionante_cedula.short_description = "Accionante cedula"

class OficioAdmin(admin.ModelAdmin):
 inlines = [ProcesoDiciplinarioInline]
 list_display=('num_fallo','accionante_cedula','accionante_nombre','accionado','asunto','fecha_envio','fecha_resp','estado','notificacion')
 raw_id_fields = ('accionante',)
 search_fields = ('num_fallo','accionante__cedula','accionante__nombre','accionado',)
 def accionante_nombre(self,obj):
     return obj.accionante.nombre
 accionante_nombre.short_description = "Accionante"
 def accionante_cedula(self, obj):
     return obj.accionante.cedula
 accionante_cedula.short_description = "Accionante cedula"
class NotificacionInline(admin.StackedInline):
  """Formulario de procesos Disciplinario"""
  model   = Notificacion
  fk_name = 'proc_discip'
  extra   = 1

class ProcesoDiciplinarioAdmin(admin.ModelAdmin):
 inlines = [NotificacionInline]

class AsuntoInline(admin.TabularInline):
  """Formulario de Victimas"""
  model = Asunto
  extra = 1

class VictimaAdmin(admin.ModelAdmin):
 inlines = [AsuntoInline]
 fieldsets = [
      ("Victimas" , {'fields': [('accionante'),'estado']})#con los parentesis se ponene los campos en la misma fila
  ]
 raw_id_fields  = ('accionante',)
 list_display   = ('accionante_cedula','accionante_nombre','estado')
 list_filter = ['estado']
 search_fields  = ['accionante__cedula','accionante__nombre']

 def accionante_nombre(self,obj):
     return obj.accionante.nombre
 accionante_nombre.short_description = "Accionante"
 def accionante_cedula(self, obj):
     return obj.accionante.cedula
 accionante_cedula.short_description = "Accionante cedula"

class TipoTutelasAdmin(admin.ModelAdmin):
  list_display   = ('nombre',)
  ordering = ('nombre',)
  search_fields  = ('nombre',)

class TipoPeticionAdmin(admin.ModelAdmin):
  list_display   = ('nombre',)
  ordering = ('nombre',)
  search_fields  = ('nombre',)

class PeticionAdmin(admin.ModelAdmin):
  raw_id_fields = ('accionante',)
  list_filter   = ['estado','tipo']
  list_display  = ('accionante_cedula','accionante_nombre','accionado','fecha_envio','estado','fecha_resp','tipo')
  search_fields = ('accionante__cedula','accionante__nombre')
  def accionante_nombre(self,obj):
     return obj.accionante.nombre
  accionante_nombre.short_description = "Accionante"
  def accionante_cedula(self, obj):
     return obj.accionante.cedula
  accionante_cedula.short_description = "Accionante cedula"


admin.site.register(Ciudadano,CiudadanoAdmin)
admin.site.register(TipoTutela,TipoTutelasAdmin)
admin.site.register(Tutela,TutelaAdmin)
admin.site.register(TipoPeticion,TipoPeticionAdmin)
admin.site.register(Peticion,PeticionAdmin)
admin.site.register(Desacato,DesacatoAdmin)
admin.site.register(Oficio,OficioAdmin)
admin.site.register(ProcesoDisciplinario,ProcesoDiciplinarioAdmin);
admin.site.register(Victima,VictimaAdmin);







