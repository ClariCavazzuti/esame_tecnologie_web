from django.shortcuts import render
from .models import MenuItem

def core(request):
    return render(request, 'core/sito-in-sviluppo.html') 

def menu(request):
    dati=MenuItem.objects.all()
    return render(request, 'core/pagina-menu.html', {'dati':dati} )