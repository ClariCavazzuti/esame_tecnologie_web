from django.shortcuts import render
from .models import MenuItem, Camera

def core(request):
    return render(request, 'core/home.html') 

def menu(request):
    menu_items = {
        'antipasti': MenuItem.objects.filter(categoria='antipasti'),
        'primi': MenuItem.objects.filter(categoria='primi'),
        'secondi': MenuItem.objects.filter(categoria='secondi'),
        'contorni': MenuItem.objects.filter(categoria='contorni'),
        'dolci': MenuItem.objects.filter(categoria='dolci'),
        'bevande': MenuItem.objects.filter(categoria='bevande'),
    }
    return render(request, 'core/pagina-menu.html', {'menu_items': menu_items} )

def camere(request):
    camere=Camera.objects.all()
    return render(request,'core/pagina-camere.html', {'camere': camere} )