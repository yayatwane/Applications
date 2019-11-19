from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from .models import document
# Create your views here.


def index(request):
    documents = document.objects.all()
    return render(request, 'index.html', {'documents': documents})
    #return HttpResponse('Hello World')

