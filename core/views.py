from django.shortcuts import render
from .models import MenuItem, Camera

def core(request):
    return render(request, 'core/sito-in-sviluppo.html') 

def menu(request):
    dati=MenuItem.objects.all()
    return render(request, 'core/pagina-menu.html', {'dati': dati} )

def camere(request):
    camere=Camera.objects.all()
    return render(request,'core/pagina-camere.html', {'camere': camere} )