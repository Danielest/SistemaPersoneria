from docs.models import *
from django.shortcuts import render_to_response

def ciudadanos(request):
	ciudadanos = Ciudadanos.objects.all()
	return render_to_response('ciudadanos.html',{'ciudadanos':ciudadanos})

