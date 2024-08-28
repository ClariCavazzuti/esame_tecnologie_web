from django.contrib import admin
from .models import Camera, RoomBooking, MenuItem, Recensione, Tavolo, Core, TavoloBooking
from datetime import datetime, timedelta
from django.db.models import Count  # Import corretto

class CameraAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo', 'camere_totali', 'riepilogo_prenotazioni')
    list_filter = ('tipo',)
    search_fields = ('nome', 'tipo', 'descrizione')

    def riepilogo_prenotazioni(self, obj):
        """
        Mostra un riepilogo di tutte le camere prenotate (per tipo) e il periodo di tempo per cui sono prenotate.
        """
        prenotazioni = RoomBooking.objects.filter(camera=obj).values('start_date', 'end_date')
        riepilogo = []
        for prenotazione in prenotazioni:
            riepilogo.append(f"{prenotazione['start_date']} - {prenotazione['end_date']}")

        return ", ".join(riepilogo) if riepilogo else "Nessuna prenotazione"

    riepilogo_prenotazioni.short_description = 'Riepilogo prenotazioni'

    def get_queryset(self, request):
        """
        Modifica la query per aggiungere eventuali annotazioni o filtraggio necessario.
        """
        qs = super().get_queryset(request)
        return qs

admin.site.register(Camera, CameraAdmin)

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

@admin.register(TavoloBooking)
class TavoloBookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'tavolo', 'data', 'orario_arrivo', 'tipo_pasto', 'numero_telefono', 'note')
    list_filter = ('data', 'tipo_pasto')
    search_fields = ('user__username', 'tavolo__numero', 'note')

@admin.register(Core)
class CoreAdmin(admin.ModelAdmin):
    list_display = ('campo1', 'campo2')
    search_fields = ('campo1', 'campo2')


