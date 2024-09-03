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
        Mostra un riepilogo delle camere prenotate, indicando quante camere sono prenotate in un dato periodo,
        tenendo conto delle sovrapposizioni.
        """
        prenotazioni = RoomBooking.objects.filter(camera=obj).order_by('start_date')
        riepilogo = []
        camere_disponibili = obj.camere_totali

        for prenotazione in prenotazioni:
            # Controlla quante camere sono prenotate nello stesso periodo
            prenotazioni_conflittuali = RoomBooking.objects.filter(
                camera=obj,
                start_date__lt=prenotazione.end_date,
                end_date__gt=prenotazione.start_date
            ).count()

            riepilogo.append(
                f"{prenotazione.start_date} - {prenotazione.end_date}: {prenotazioni_conflittuali} camere occupate su {camere_disponibili}"
            )

        return ", ".join(riepilogo) if riepilogo else "Nessuna prenotazione"

    riepilogo_prenotazioni.short_description = 'Riepilogo prenotazioni'

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
    ordering = ['-created_at']  # Ordina per data decrescente come predefinito
    sortable_by = ('voto', 'created_at')  # Permette l'ordinamento per voto o data

@admin.register(Tavolo)
class TavoloAdmin(admin.ModelAdmin):
    list_display = ('numero', 'posti')  # Rimuovi 'disponibile'
    list_filter = ('numero',)

    
@admin.register(TavoloBooking)
class TavoloBookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'tavolo', 'data', 'orario_arrivo', 'tipo_pasto', 'numero_telefono', 'email', 'note')
    list_filter = ('data', 'tipo_pasto')
    search_fields = ('user__username', 'tavolo__numero', 'note', 'email')
    ordering = ['data']  # Ordina per data in modo crescente




