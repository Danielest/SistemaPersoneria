from django.contrib import admin
from django import forms 
from docs.models import *

import datetime


class CiudadanoAdmin(admin.ModelAdmin):
  fieldsets = [
    ('Informacion Personal' , {
      'fields':[('nombre', 'apellido1','apellido2'),'cedula','tel','email']}),#con los parentesis se ponene los campos en la misma fila
    ('Localidad'            , {'fields':['barrio','direccion']})
  ]
  list_display = ('nombreCompleto','cedula')
  search_fields = ['cedula','nombre']
  ordering = ("nombre","apellido1","apellido2","cedula")


class TutelaForm(forms.ModelForm):
  # fecha_envio = forms.DateField(initial=datetime.date.today)
  class Meta:
    model = Tutela
  # Methods
  def clean(self):
    fecha_envio = self.cleaned_data['fecha_envio']
    fecha_resp = self.cleaned_data['fecha_resp']
    if fecha_envio < datetime.date.today():
      self._errors['fecha_envio'] = self.error_class(["El dia no puede ser antes de la fecha actual."]) 
    if fecha_resp < fecha_envio:
      self._errors['fecha_resp'] = self.error_class(["La fehca de respuesta debe ser despues del dia "])
    del self.cleaned_data['fecha_envio']
    del self.cleaned_data['fecha_resp']
    return self.cleaned_data
    

class TutelaAdmin(admin.ModelAdmin):
  change_list_template = "admin/change_list_filter_sidebar.html"
  change_list_filter_template = "admin/filter_listing.html"
  form = TutelaForm
  fieldset = [
     ("Tutela" , {'fields': ['accionante','accionado','tipo','fecha_envio','fecha_resp','estado','adjunto']})
   ]
  raw_id_fields  = ('accionante',)#esto es para que aparezca un campo de busqueda en vez de un select
  autocomplete_lookup_fields = {
        'fk': ['accionante'],
  }
  list_display   = ('accionante_cedula','accionante_nombre','accionado','tipo','fecha_envio','fecha_resp','estado')
  date_hierarchy = 'fecha_envio'
  search_fields  = ['accionado','accionante__cedula','accionante__nombre']# para que pueda buscar por llave foranea toca poner modelo__campo
  list_filter = ['estado','tipo']
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
  change_list_template = "admin/change_list_filter_sidebar.html"
  change_list_filter_template = "admin/filter_listing.html"
  fieldsets = [
      ("Desacato" , {'fields': ['accionante','accionado','tipo','fecha_envio','fecha_resp','estado','adjunto']})#con los parentesis se ponene los campos en la misma fila
  ]
  raw_id_fields  = ('accionante',)
  autocomplete_lookup_fields = {
        'fk': ['accionante'],
  }
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
 autocomplete_lookup_fields = {
        'fk': ['accionante'],
  }
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
 list_display   = ('ent_notific','estado','fecha_envio','fecha_resp','investigacion')
 #

class AsuntoInline(admin.TabularInline):
  """Formulario de Victimas"""
  model = Asunto
  extra = 1

class VictimaAdmin(admin.ModelAdmin):
 change_list_template = "admin/change_list_filter_sidebar.html"
 change_list_filter_template = "admin/filter_listing.html"
 inlines = [AsuntoInline]
 fieldsets = [
      ("Victimas" , {'fields': [('accionante'),'estado']})#con los parentesis se ponene los campos en la misma fila
  ]
 raw_id_fields  = ('accionante',)
 autocomplete_lookup_fields = {
        'fk': ['accionante'],
  }
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
  change_list_template = "admin/change_list_filter_sidebar.html"
  change_list_filter_template = "admin/filter_listing.html"
  raw_id_fields = ('accionante',)
  list_filter   = ['estado','tipo']
  list_display  = ('accionante_cedula','accionante_nombre','accionado','fecha_envio','estado','fecha_resp','tipo')
  search_fields = ('accionante__cedula','accionante__nombre')
  autocomplete_lookup_fields = {
        'fk': ['accionante'],
  }
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







