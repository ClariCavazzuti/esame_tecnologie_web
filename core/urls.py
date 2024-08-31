from django.urls import  path
from . import views

urlpatterns = [
    path('', views.core, name='core_home'),
    path('menu', views.menu, name='menu'),
    path('camere', views.camere, name='camere'),
    path('book_room/<int:camera_id>/', views.book_room, name='book_room'),
    path('search_rooms', views.search_rooms, name='search_rooms'),
    path('confirm_booking/', views.confirm_booking, name='confirm_booking'),
    path('booking_success/', views.booking_success, name='booking_success'),
    path('cancella_prenotazione/<int:prenotazione_id>/', views.cancella_prenotazione, name='cancella_prenotazione'),
    path('prenotazione_tavolo/', views.prenotazione_tavolo, name='prenotazione_tavolo'),
    path('area_personale',views.area_personale, name='area_personale'),
    path('recensioni', views.recensione, name='recensioni'),
    path('aggiungi-recensione/', views.aggiungi_recensione, name='aggiungi_recensione'),
]
