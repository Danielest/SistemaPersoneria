from django.contrib import admin
from docs.models import *
from forms import *



class CiudadanoAdmin(admin.ModelAdmin):
  fieldsets = [
    ('Informacion Personal' , {
      'fields':['nombre',('apellido1','apellido2'),'cedula','tel','email']}),#con los parentesis se ponene los campos en la misma fila
    ('Localidad', {'fields':['barrio','direccion']})
  ]
  list_display = ('nombreCompleto','cedula')
  ordering = ("nombre","apellido1","apellido2","cedula")
  search_fields = ['cedula','nombre']

#TUTELAS

class TipoTutelasAdmin(admin.ModelAdmin):
  list_display   = ('nombre',)
  ordering = ('nombre',)
  search_fields  = ('nombre',)

class TutelaAdmin(admin.ModelAdmin):
  autocomplete_lookup_fields = {
        'fk': ['accionante'],
  }
  change_list_template = "admin/change_list_filter_sidebar.html"
  change_list_filter_template = "admin/filter_listing.html"
  date_hierarchy = 'fecha_envio'
  form = TutelaForm
  fieldsets = [
     ("Modulo Tutela" , {
        'fields': ['accionante','accionado','tipo','estado','fecha_envio','fecha_resp','adjunto']})
   ]
  list_display   = ('accionante_cedula','accionado','tipo','fecha_envio','fecha_resp','estado','tieneAdjunto','id')
  list_filter = ['estado','tipo']
  ordering = ('fecha_envio','fecha_resp')
  raw_id_fields  = ('accionante',)#esto es para que aparezca un campo de busqueda en vez de un select
  search_fields  = ['accionado','accionante__cedula']# para que pueda buscar por llave foranea toca poner modelo__campo
  def accionante_nombre(self,obj):
    return obj.accionante.nombre
  accionante_nombre.short_description = "Accionante"
  def accionante_cedula(self, obj):
    return obj.accionante.cedula
  accionante_cedula.short_description = "Accionante cedula"


#PETICIONES

class TipoPeticionAdmin(admin.ModelAdmin):
  list_display   = ('nombre',)
  ordering = ('nombre',)
  search_fields  = ('nombre',)


class PeticionAdmin(admin.ModelAdmin):
  autocomplete_lookup_fields = {
        'fk': ['accionante'],
  }
  change_list_template = "admin/change_list_filter_sidebar.html"
  change_list_filter_template = "admin/filter_listing.html"
  form = PeticionForm
  fieldsets = [
     ("Modulo Peticion" , {
        'fields': ['accionante','accionado','tipo','estado','fecha_envio','fecha_resp','adjunto']})
  ]
  list_filter   = ['estado','tipo']
  list_display  = ('accionante_cedula','accionado','fecha_envio','fecha_resp','estado','tipo','tieneAdjunto','id')
  raw_id_fields = ('accionante',)
  search_fields = ('accionante__cedula',)
  def accionante_nombre(self,obj):
     return obj.accionante.nombre
  accionante_nombre.short_description = "Accionante"
  def accionante_cedula(self, obj):
     return obj.accionante.cedula
  accionante_cedula.short_description = "Accionante cedula"

#DESACATOS

class DesacatoAdmin(admin.ModelAdmin):
  autocomplete_lookup_fields = {
        'fk': ['accionante'],
  }
  change_list_template = "admin/change_list_filter_sidebar.html"
  change_list_filter_template = "admin/filter_listing.html"
  date_hierarchy = 'fecha_envio'
  form = DesacatoForm
  fieldsets = [
      ("Desacato" , {'fields': ['accionante','accionado','fecha_envio','fecha_resp','tipo','estado','adjunto']})#con los parentesis se ponene los campos en la misma fila
  ]
  list_display   = ('accionante_cedula','accionado','fecha_envio','fecha_resp','tipo','estado','tieneAdjunto','id')
  list_filter = ['estado']
  raw_id_fields  = ('accionante',)
  search_fields  = ['accionado','accionante__cedula',]
  def accionante_nombre(self,obj):
     return obj.accionante.nombre
  accionante_nombre.short_description = "Accionante"
  def accionante_cedula(self, obj):
     return obj.accionante.cedula
  accionante_cedula.short_description = "Accionante cedula"

#OFICIOS

class ProcesoDiciplinarioInline(admin.StackedInline):
  """Formulario de oficios"""
  model   = ProcesoDisciplinario
  title = "Generar Procesos Diciplinarios"
  fk_name = 'oficio'
  extra   = 1
  fieldsets = [
      (None , {'fields': ['ent_notific','fecha_envio','fecha_resp','investigacion','estado','adjunto',]})#con los parentesis se ponene los campos en la misma fila
  ]

class OficioAdmin(admin.ModelAdmin):
 autocomplete_lookup_fields = {
        'fk': ['accionante'],
  }
 change_list_template = "admin/change_list_filter_sidebar.html"
 change_list_filter_template = "admin/filter_listing.html"
 date_hierarchy = 'fecha_envio' 
 fieldsets = [
      ("Oficio" , {'fields': ['accionante','accionado','num_fallo','fecha_envio','fecha_resp','estado','asunto','notificacion','adjunto']})#con los parentesis se ponene los campos en la misma fila
 ] 
 form = OficioForm
 inlines = [ProcesoDiciplinarioInline]
 list_display=('num_fallo','accionante_cedula','accionado','fecha_envio','fecha_resp','asunto','estado','tieneAdjunto','id')
 list_filter = ['estado']
 raw_id_fields = ('accionante',)
 search_fields  = ['num_fallo','accionado','asunto']
 def accionante_nombre(self,obj):
     return obj.accionante.nombre
 accionante_nombre.short_description = "Accionante"
 def accionante_cedula(self, obj):
     return obj.accionante.cedula
 accionante_cedula.short_description = "Accionante cedula"

#PROCESOS DICIPLINARIOS

class NotificacionInline(admin.StackedInline):
  """Formulario de procesos Disciplinario"""
  model   = Notificacion
  fk_name = 'proc_discip'
  extra   = 1


class ProcesoDiciplinarioAdmin(admin.ModelAdmin):
 autocomplete_lookup_fields = {
        'fk': ['oficio'],
 } 
 change_list_template = "admin/change_list_filter_sidebar.html"
 change_list_filter_template = "admin/filter_listing.html" 
 date_hierarchy = 'fecha_envio'
 inlines = [NotificacionInline]
 Form = ProcesoDiciplinarioForm
 form = ProcesoDiciplinarioForm
 fieldsets = [
      ("Oficio" , {'fields': ['oficio','ent_notific','fecha_envio','fecha_resp','investigacion','estado','adjunto']})#con los parentesis se ponene los campos en la misma fila
 ]
 list_display   = ('ent_notific','fecha_envio','fecha_resp','investigacion','estado','getOficio','id')
 list_filter = ['estado','investigacion']
 raw_id_fields = ('oficio',)
 search_fields  = ['accionado','accionante__cedula','asunto','num_fallo']
#VICTIMAS

class AsuntoInline(admin.TabularInline):
  """Formulario de Victimas"""
  model = Asunto
  extra = 1
  fieldsets = [
      ("Victimas" , {'fields': ['nombre','fecha_envio','adjunto']})#con los parentesis se ponene los campos en la misma fila
   ]

class VictimaAdmin(admin.ModelAdmin):
 change_list_template = "admin/change_list_filter_sidebar.html"
 change_list_filter_template = "admin/filter_listing.html"
 inlines = [AsuntoInline]
 fieldsets = [
      ("Victimas" , {'fields': [('accionante','estado'),'fecha_envio']})#con los parentesis se ponene los campos en la misma fila
  ]
 raw_id_fields  = ('accionante',)
 autocomplete_lookup_fields = {
        'fk': ['accionante'],
  }
 list_display   = ('accionante_cedula','accionante_nombre','estado','id')
 list_filter = ['estado']
 search_fields  = ['accionante__cedula','accionante__nombre']
 def accionante_nombre(self,obj):
     return obj.accionante.nombre
 accionante_nombre.short_description = "Accionante Nombre"
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







