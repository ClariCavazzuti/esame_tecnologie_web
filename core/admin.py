from django.contrib import admin
from .models import Camera, RoomBooking, MenuItem, Recensione, Tavolo, Core

@admin.register(Camera)
class CameraAdmin(admin.ModelAdmin):
    list_display = ('tipo', 'camere_totali', 'numero_posti_letto', 'prezzo_per_notte')
    list_filter = ('tipo',)
    search_fields = ('tipo', 'descrizione')

@admin.register(RoomBooking)
class RoomBookingAdmin(admin.ModelAdmin):
    list_display = ('utente', 'camera', 'start_date', 'end_date', 'created_at')
    list_filter = ('camera', 'start_date', 'end_date')
    search_fields = ('utente__username', 'camera__tipo')

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('nome', 'categoria', 'prezzo')
    list_filter = ('categoria',)
    search_fields = ('nome', 'descrizione')

@admin.register(Recensione)
class RecensioneAdmin(admin.ModelAdmin):
    list_display = ('utente', 'voto', 'created_at')
    list_filter = ('voto', 'created_at')
    search_fields = ('utente__username', 'commento')

@admin.register(Tavolo)
class TavoloAdmin(admin.ModelAdmin):
    list_display = ('numero', 'posti', 'disponibile')
    list_filter = ('posti', 'disponibile')
    search_fields = ('numero',)

@admin.register(Core)
class CoreAdmin(admin.ModelAdmin):
    list_display = ('campo1', 'campo2')
    search_fields = ('campo1', 'campo2')
