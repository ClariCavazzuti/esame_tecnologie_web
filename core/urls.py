from django.urls import  path
from . import views

urlpatterns = [
    path('', views.core, name='core_home'),
    path('menu', views.menu, name='menu'),
    path('camere', views.camere, name='camere'),
]
