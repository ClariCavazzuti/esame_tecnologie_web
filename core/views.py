from django.shortcuts import render
from .models import core
def core(request):
    dati=core.objects.all()
    return render(request, 'core/sito-in-sviluppo.html',{'dato':dati}) 

