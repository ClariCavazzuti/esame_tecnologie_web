from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from core.forms import CustomUserCreationForm
from django.shortcuts import render
from django.http import JsonResponse


class UserCreateView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "core/user_create.html"
    success_url = reverse_lazy("login")

def inactive_logout(request):
    return render(request, 'core/inactive_logout.html')

def check_session():
    # Implementa la logica per determinare se la sessione è attiva
    is_active = True  # Imposta questa variabile in base alla logica della tua applicazione
    return JsonResponse({'is_active': is_active})