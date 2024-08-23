from django.urls import include, path
from django.contrib import admin
from . import views 

app_name = 'core'

urlpatterns = [
    path('core/', views.core ),
    path('admin/', admin.site.urls),

]