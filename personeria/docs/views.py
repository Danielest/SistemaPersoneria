# Create your views here.
from django.http import HttpResponse
from django.template import Context, loader #1) una forma de hacerlo
from django.shortcuts import render         #2) segunda forma de hacerlo
from docs.models import Tutela


def index(request):
  tutelas_list = Tutela.objects.order_by('-fecha_envio')[:5]
  output = ' , '.join([p.estado for p in tutelas_list])
  return HttpResponse(output)

def indexCiudadano(request):
  return HttpResponse("Todos los ciudadanos")

def singleCiudadano(request, ciud_id):
  return HttpResponse("Ciudadano especifico")

# 1)esta es una primera forma de hacer el render de la platilla
# def indexTutela(request):
#   tutelas_list = Tutela.objects.order_by('-fecha_envio')[:5]
#   template = loader.get_template('docs/index.html')
#   context = Context({'tutelas_list' : tutelas_list})
#   return HttpResponse(template.render(context))

# esta es la segunda forma
def indexTutela(request):
  tutelas_list = Tutela.objects.order_by('-fecha_envio')[:5]
  context = {'tutelas_list' : tutelas_list}
  return render(request,'docs/tutela/index.html',context)

def singleTutela(request, tut_id):
  try:
    tutela = Tutela.objects.get(pk=tut_id)
  except Tutela.DoesNotExist:
    raise Http404
  return render(request,"docs/tutela/tutela.html",{'tutela': tutela})

from reportlab.pdfgen import canvas
from django.http import HttpResponse


# pip instal reportLab https://docs.djangoproject.com/en/dev/howto/outputting-pdf/
def pruebapdf(request):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'

    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 100, "Hello world.")

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()
    return response

