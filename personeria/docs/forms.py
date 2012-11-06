from django import forms 
from docs.models import Tutela,Peticion,Desacato,Oficio,ProcesoDisciplinario
import datetime
from django.utils import timezone

#TUTELAS
class TutelaForm(forms.ModelForm):
  class Meta:
    model = Tutela
  # Methods
  # la forma de validar se encuentra en https://docs.djangoproject.com/en/dev/ref/forms/validation/
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
  # class Media:
  #   js = ["/media/js/validators.js",]

#PETICIONES

class PeticionForm(forms.ModelForm):
  class Meta:
    model = Peticion
  # Methods
  # la forma de validar se encuentra en https://docs.djangoproject.com/en/dev/ref/forms/validation/
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

#DESACATOS

class DesacatoForm(forms.ModelForm):
  class Meta:
    model = Desacato
  # Methods
  # la forma de validar se encuentra en https://docs.djangoproject.com/en/dev/ref/forms/validation/
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
    
#OFICIO

class OficioForm(forms.ModelForm):
  class Meta:
    model = Oficio
  # Methods
  # la forma de validar se encuentra en https://docs.djangoproject.com/en/dev/ref/forms/validation/
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
     
#PROCESODICIPLINARIO

class ProcesoDiciplinarioForm(forms.ModelForm):
  class Meta:
    model = ProcesoDisciplinario
  # Methods
  # la forma de validar se encuentra en https://docs.djangoproject.com/en/dev/ref/forms/validation/
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


