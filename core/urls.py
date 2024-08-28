from django.urls import  path
from . import views

urlpatterns = [
    path('', views.core, name='core_home'),
    path('menu', views.menu, name='menu'),
    path('camere', views.camere, name='camere'),
    path('book_room/<int:camera_id>/', views.book_room, name='book_room'),
    path('room_details/', views.room_details, name='room_details'),
    path('search_rooms/', views.search_rooms, name='search_rooms'),

]
