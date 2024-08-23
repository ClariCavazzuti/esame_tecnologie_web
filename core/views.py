from django.shortcuts import render

def core(request):
    return render(request, 'core/sito-in-sviluppo.html')
