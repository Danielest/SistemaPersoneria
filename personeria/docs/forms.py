from django import forms 
from docs.models import Tutela
import datetime

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


