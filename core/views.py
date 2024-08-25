from django.shortcuts import render
from .models import MenuItem

def core(request):
    dati=MenuItem.objects.all()
    return render(request, 'core/pagina-menu.html',{'dati':dati}) 

