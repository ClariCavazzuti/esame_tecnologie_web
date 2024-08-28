from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import MenuItem, Camera, RoomBooking
from .forms import RoomSearchForm, RoomBookingForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import date

def core(request):
    return render(request, 'core/home.html') 

def menu(request):
    menu_items = {
        'antipasti': MenuItem.objects.filter(categoria='antipasti'),
        'primi': MenuItem.objects.filter(categoria='primi'),
        'secondi': MenuItem.objects.filter(categoria='secondi'),
        'contorni': MenuItem.objects.filter(categoria='contorni'),
        'dolci': MenuItem.objects.filter(categoria='dolci'),
        'bevande': MenuItem.objects.filter(categoria='bevande'),
    }
    return render(request, 'core/pagina-menu.html', {'menu_items': menu_items} )

def camere(request):
    camere=Camera.objects.all()
    return render(request,'core/pagina-camere.html', {'camere': camere} )

def room_details(request):
    """
    Vista per visualizzare i dettagli dei tipi di camere. Mostra tutte le tipologie di camere.
    """
    room_types = Camera.objects.all()
    return render(request, 'core/room_details.html', {'room_types': room_types})


@login_required
def book_room(request, camera_id):
    """
    Vista per la prenotazione di una camera. Solo utenti registrati possono effettuare prenotazioni.
    """
    camera = get_object_or_404(Camera, id=camera_id)
    if request.method == 'POST':
        form = RoomBookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.utente = request.user
            booking.camera = camera
            booking.save()
            return redirect('booking_list')  # Assicurati di avere una vista e un URL definiti per 'booking_list'
    else:
        form = RoomBookingForm()
    
    return render(request, 'core/book_room.html', {'form': form, 'camera': camera})



def search_rooms(request):
    """
    Vista per la ricerca di camere disponibili in base alle date e al numero di posti letto.
    """
    if request.method == 'GET':
        form = RoomSearchForm(request.GET)
        if form.is_valid():
            check_in_date = form.cleaned_data['check_in_date']
            check_out_date = form.cleaned_data['check_out_date']
            posti_letto = form.cleaned_data['posti_letto']

            # Filtra le camere che hanno il numero di posti letto richiesto
            # e non hanno prenotazioni che si sovrappongono alle date di ricerca
            available_rooms = Camera.objects.filter(
                numero_posti_letto__gte=posti_letto
            ).exclude(
                
            ).distinct()

            return render(request, 'core/room_search_results.html', {'available_rooms': available_rooms})
    else:
        form = RoomSearchForm()
    return render(request, 'core/search_rooms.html', {'form': form})


@csrf_exempt
@login_required

def ajax_book_room(request):
    """
    Vista per gestire la prenotazione di una camera tramite una richiesta AJAX.
    """
    if request.method == 'POST':
        camera_id = request.POST.get('camera_id')
        check_in_date = request.POST.get('check_in_date')
        check_out_date = request.POST.get('check_out_date')
        utente = request.user

        # Recupera la camera
        camera = get_object_or_404(Camera, id=camera_id)

        # Crea una nuova prenotazione
        booking = RoomBooking.objects.create(
            utente=utente,
            camera=camera,
            start_date=check_in_date,
            end_date=check_out_date
        )

        return JsonResponse({'success': True, 'message': 'Prenotazione effettuata con successo!'})

    return JsonResponse({'success': False, 'message': 'Metodo non consentito'})


@csrf_exempt
@login_required
def ajax_book_rooms(request):
    """
    Vista per gestire la prenotazione di più camere tramite una richiesta AJAX.
    """
    if request.method == 'POST':
        camera_ids = request.POST.get('camera_ids').split(',')
        check_in_date = request.POST.get('check_in_date')
        check_out_date = request.POST.get('check_out_date')
        utente = request.user

        # Controllo disponibilità e prenotazione
        camere_prenotate = []
        for camera_id in camera_ids:
            camera = get_object_or_404(Camera, id=camera_id)
            if camera.camere_totali > 0:  # Verifica se ci sono camere disponibili
                RoomBooking.objects.create(
                    utente=utente,
                    camera=camera,
                    start_date=check_in_date,
                    end_date=check_out_date
                )
                camera.decrementa_camere_disponibili()  # Decrementa il numero di camere disponibili
                camere_prenotate.append(camera.nome)
            else:
                return JsonResponse({'success': False, 'message': f'Nessuna camera disponibile per il tipo {camera.nome}'})

        return JsonResponse({'success': True, 'message': 'Prenotazione effettuata con successo per le seguenti camere: ' + ', '.join(camere_prenotate)})

    return JsonResponse({'success': False, 'message': 'Metodo non consentito'})

@login_required
def cancella_prenotazione(request, prenotazione_id):
    """
    Vista per cancellare una prenotazione.
    Incrementa il numero di camere disponibili del tipo corrispondente.
    """
    prenotazione = get_object_or_404(RoomBooking, id=prenotazione_id, utente=request.user)

    # Incrementa il numero di camere disponibili
    camera = prenotazione.camera
    camera.camere_totali += 1
    camera.save()

    # Elimina la prenotazione
    prenotazione.delete()

    # Messaggio di successo
    messages.success(request, 'Prenotazione cancellata con successo.')

    # Redirect alla lista delle prenotazioni o alla home
    return redirect('core_home')