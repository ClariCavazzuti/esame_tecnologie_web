from django.shortcuts import render
from .models import Core

def core(request):
    dati=Core.objects.all()
    return render(request, 'core/sito-in-sviluppo.html',{'dato':dati}) 

