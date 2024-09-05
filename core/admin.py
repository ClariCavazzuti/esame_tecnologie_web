from django.contrib import admin
from .models import Camera, RoomBooking, MenuItem, Recensione, Tavolo, TavoloBooking
from django.db.models import Count 


class CameraAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo', 'camere_totali', 'riepilogo_prenotazioni')
    list_filter = ('tipo',)
    search_fields = ('nome', 'tipo', 'descrizione')

    def riepilogo_prenotazioni(self, obj):
        """
        Mostra un riepilogo delle camere prenotate, indicando quante camere sono prenotate in un dato periodo,
        tenendo conto delle sovrapposizioni.
        """
        # Recuperiamo tutte le prenotazioni della camera corrente e ordiniamo per data di inizio
        prenotazioni = RoomBooking.objects.filter(camera=obj).order_by('start_date')

        # Pre-carichiamo tutte le prenotazioni sovrapposte per ridurre le query
        prenotazioni_conflittuali = RoomBooking.objects.filter(camera=obj).values('start_date', 'end_date')

        riepilogo = []
        camere_totali = obj.camere_totali

        for prenotazione in prenotazioni:
            # Calcoliamo le prenotazioni sovrapposte direttamente nel loop
            prenotazioni_in_conflitto = sum(
                1 for p in prenotazioni_conflittuali
                if p['start_date'] < prenotazione.end_date and p['end_date'] > prenotazione.start_date
            )
            
            riepilogo.append(
                f"{prenotazione.start_date} - {prenotazione.end_date}: {prenotazioni_in_conflitto} camere occupate su {camere_totali}"
            )

        return ", ".join(riepilogo) if riepilogo else "Nessuna prenotazione"

    riepilogo_prenotazioni.short_description = 'Riepilogo prenotazioni'  # Questo definisce la descrizione che appare nell'admin

    def get_queryset(self, request):
        """
        Modifica la query per aggiungere eventuali annotazioni o filtraggio necessario.
        """
        qs = super().get_queryset(request)
        return qs.annotate(num_prenotazioni=Count('roombooking')).order_by('-num_prenotazioni')

admin.site.register(Camera, CameraAdmin)


@admin.register(RoomBooking)
class RoomBookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'camera', 'start_date', 'end_date', 'created_at', 'email', 'numero_telefono', 'note')
    list_filter = ('camera', 'start_date', 'end_date')
    search_fields = ('user__username', 'camera__tipo', 'email')

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('nome', 'categoria', 'prezzo')
    list_filter = ('categoria',)
    search_fields = ('nome', 'descrizione')

@admin.register(Recensione)
class RecensioneAdmin(admin.ModelAdmin):
    list_display = ('user', 'voto', 'created_at')
    list_filter = ('voto', 'created_at')
    search_fields = ('user__username', 'commento')
    ordering = ['-created_at'] 
    sortable_by = ('voto', 'created_at') 

@admin.register(Tavolo)
class TavoloAdmin(admin.ModelAdmin):
    list_display = ('numero', 'posti') 
    list_filter = ('numero',)

    
@admin.register(TavoloBooking)
class TavoloBookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'tavolo', 'data', 'orario_arrivo', 'tipo_pasto', 'numero_telefono', 'email', 'note')
    list_filter = ('data', 'tipo_pasto')
    search_fields = ('user__username', 'tavolo__numero', 'note', 'email')
    ordering = ['data']  




