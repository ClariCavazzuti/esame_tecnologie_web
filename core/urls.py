from django.urls import  path
from . import views

urlpatterns = [
    path('', views.core, name='core_home'),
    path('menu', views.menu, name='menu'),
    path('camere', views.camere, name='camere'),
    path('book_room/<int:camera_id>/', views.book_room, name='book_room'),
    path('search_rooms', views.search_rooms, name='search_rooms'),
    path('ajax/book_room/', views.ajax_book_room, name='ajax_book_room'),
    path('ajax/book_rooms/', views.ajax_book_rooms, name='ajax_book_rooms'),
    path('cancella_prenotazione/<int:prenotazione_id>/', views.cancella_prenotazione, name='cancella_prenotazione'),
]
