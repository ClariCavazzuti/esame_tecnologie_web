from django.contrib import admin
from .models import Camera, RoomBooking, MenuItem, Recensione, Tavolo, Core
from datetime import datetime, timedelta

class CameraAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo', 'camere_totali', 'camere_prenotate_settimana')
    list_filter = ('tipo',)
    search_fields = ('nome', 'tipo', 'descrizione')

    def camere_prenotate_settimana(self, obj):
        """
        Calcola e mostra quante camere di questo tipo sono prenotate nella settimana corrente.
        """
        oggi = datetime.today()
        inizio_settimana = oggi - timedelta(days=oggi.weekday())
        fine_settimana = inizio_settimana + timedelta(days=6)

        # Filtra le prenotazioni che iniziano o finiscono in questa settimana
        prenotazioni = RoomBooking.objects.filter(
            camera=obj,
            start_date__lte=fine_settimana,
            end_date__gte=inizio_settimana
        )
        
        return prenotazioni.count()
    
    camere_prenotate_settimana.short_description = 'Camere prenotate (questa settimana)'

    def show_bookings_for_week(self, request, queryset):
        """
        Azione personalizzata per mostrare le prenotazioni per una settimana selezionata.
        """
        settimana = request.GET.get('settimana')
        if settimana:
            try:
                inizio_settimana = datetime.strptime(settimana + '-1', "%Y-W%W-%w")
                fine_settimana = inizio_settimana + timedelta(days=6)
            except ValueError:
                self.message_user(request, "Formato data non valido", level='error')
                return

            # Calcola le prenotazioni per ogni camera selezionata
            risultato = []
            for camera in queryset:
                prenotazioni = RoomBooking.objects.filter(
                    camera=camera,
                    start_date__lte=fine_settimana,
                    end_date__gte=inizio_settimana
                ).count()
                risultato.append(f"{camera.nome} ({camera.tipo}): {prenotazioni} prenotazioni")

            self.message_user(request, "\n".join(risultato))

        else:
            self.message_user(request, "Seleziona una settimana per vedere le prenotazioni", level='error')

    show_bookings_for_week.short_description = 'Mostra prenotazioni per settimana selezionata'

    def get_queryset(self, request):
        """
        Modifica la query per aggiungere il conteggio delle camere prenotate.
        """
        qs = super().get_queryset(request)
        # Esegue una annotazione delle prenotazioni per ogni camera
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

@admin.register(Core)
class CoreAdmin(admin.ModelAdmin):
    list_display = ('campo1', 'campo2')
    search_fields = ('campo1', 'campo2')
