from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from core.forms import CustomUserCreationForm
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

class UserCreateView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "core/user_create.html"
    success_url = reverse_lazy("login")

def inactive_logout(request):
    return render(request, 'core/inactive_logout.html')


@login_required
def check_session():
    return JsonResponse({'is_active': True})