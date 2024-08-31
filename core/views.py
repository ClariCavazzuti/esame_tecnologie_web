from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import MenuItem, Camera, RoomBooking, TavoloBooking, Tavolo, Recensione
from .forms import RoomSearchForm, RoomBookingForm, TavoloBookingForm, RecensioneForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.contrib import messages 
from django.core.exceptions import ValidationError

# Funzione di utilità per verificare la disponibilità delle camere
def check_availability(camera, start_date, end_date):
    bookings = RoomBooking.objects.filter(
        camera=camera,
        start_date__lt=end_date,
        end_date__gt=start_date
    )
    return bookings.count() < camera.camere_totali

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
    return render(request, 'core/pagina-menu.html', {'menu_items': menu_items})

def recensione(request):
    recensioni={
        Recensione.objects.all(),
    }
    return render(request,'core/recensioni.html', {'recensioni' : recensioni})

@login_required
def aggiungi_recensione(request):
    if request.method == 'POST':
        form = RecensioneForm(request.POST, request.FILES)
        if form.is_valid():
            recensione = form.save(commit=False) #creo la recensione senza salvarla 
            recensione.user = request.user
            #recensione.clean()
            recensione.save()
            return redirect('core_home')
    
    else:
        form = RecensioneForm()
    
    return render(request, 'core/aggiungi_recensione.html', {'form': form})


def camere(request):
    camere = Camera.objects.all()
    return render(request, 'core/pagina-camere.html', {'camere': camere})


@login_required
def book_room(request, camera_id):
    camera = get_object_or_404(Camera, id=camera_id)
    if request.method == 'POST':
        form = RoomBookingForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            if check_availability(camera, start_date, end_date):
                booking = form.save(commit=False)
                booking.user = request.user
                booking.camera = camera
                booking.save()
                messages.success(request, 'Prenotazione effettuata con successo.')
                return redirect('booking_list')
            else:
                messages.error(request, 'La camera non è disponibile per il periodo selezionato.')
        else:
            messages.error(request, 'Ci sono errori nel modulo. Per favore correggili.')
    else:
        form = RoomBookingForm()
    return render(request, 'core/book_room.html', {'camera': camera, 'form' : form})

def booking_success(request):
    return render(request, 'core/booking_success.html')

def area_personale(request):
    return render(request, 'core/area_personale.html')

def search_rooms(request):
    if request.method == 'POST':
        form = RoomSearchForm(request.POST)
        if form.is_valid():
            check_in_date = form.cleaned_data['check_in_date']
            check_out_date = form.cleaned_data['check_out_date']
            posti_letto = form.cleaned_data['posti_letto']

            # Filtra le camere in base ai posti letto
            available_rooms = Camera.objects.filter(
                numero_posti_letto__gte=posti_letto
            )

            # Filtra ulteriormente per disponibilità
            available_rooms = [camera for camera in available_rooms if check_availability(camera, check_in_date, check_out_date)]

            if not available_rooms:
                messages.error(request, 'Nessuna camera disponibile per le date e il numero di posti letto selezionati.')
            else:
                # Passa le date come parametri alla prossima view
                return render(request, 'core/room_search_results.html', {
                    'available_rooms': available_rooms,
                    'check_in_date': check_in_date,
                    'check_out_date': check_out_date,
                })

    else:
        form = RoomSearchForm()
    return render(request, 'core/search_rooms.html', {'form': form})

@login_required
def confirm_booking(request):
    if request.method == 'POST':
        selected_room_ids = request.POST.getlist('camere')
        check_in_date = request.POST.get('check_in_date')
        check_out_date = request.POST.get('check_out_date')
        numero_telefono = request.POST.get('numero_telefono')
        note = request.POST.get('note')

        # Converte le stringhe delle date in oggetti datetime.date
        try:
            check_in_date = datetime.strptime(check_in_date, '%Y-%m-%d').date()
            check_out_date = datetime.strptime(check_out_date, '%Y-%m-%d').date()
        except ValueError:
            messages.error(request, 'Il formato della data non è valido.')
            return redirect('search_rooms')
        
        if not selected_room_ids:
            messages.error(request, 'Seleziona almeno una camera per procedere con la prenotazione.')
            return redirect('search_rooms')

        # Effettua la prenotazione per ogni camera selezionata
        for room_id in selected_room_ids:
            camera = get_object_or_404(Camera, id=room_id)
            if check_availability(camera, check_in_date, check_out_date):
                RoomBooking.objects.create(
                    user=request.user,
                    camera=camera,
                    start_date=check_in_date,
                    end_date=check_out_date,
                    numero_telefono=numero_telefono,
                    email=request.user.email,
                    note=note
                )
            else:
                messages.error(request, f"La camera {camera.nome} non è più disponibile per le date selezionate.")
                return redirect('search_rooms')
        
        messages.success(request, 'Prenotazione effettuata con successo!')
        return redirect('booking_success')
    return redirect('search_rooms')


@login_required
def cancella_prenotazione(request, prenotazione_id):
    prenotazione = get_object_or_404(RoomBooking, id=prenotazione_id, utente=request.user)
    camera = prenotazione.camera
    camera.incrementa_camere_disponibili()
    prenotazione.delete()
    messages.success(request, 'Prenotazione cancellata con successo.')
    return redirect('core_home')


@login_required
def prenotazione_tavolo(request):
    if request.method == 'POST':
        form = TavoloBookingForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data['data']
            tipo_pasto = form.cleaned_data['tipo_pasto']
            numero_persone = form.cleaned_data['numero_persone']

            tavolo_disponibile = Tavolo.objects.exclude(
                tavolobooking__data=data,
                tavolobooking__tipo_pasto=tipo_pasto
            ).filter(posti__gte=numero_persone).first()

            if tavolo_disponibile:
                booking = form.save(commit=False)
                booking.user = request.user
                booking.tavolo = tavolo_disponibile
                booking.save()
                return JsonResponse({'success': True, 'message': 'Tavolo prenotato con successo!'})

            else:
                form.add_error(None, 'Nessun tavolo disponibile per la data e il tipo di pasto selezionati.')
                return JsonResponse({'success': False, 'message': 'Nessun tavolo disponibile per la data e il tipo di pasto selezionati.'})
        else:
            return JsonResponse({'success': False, 'message': 'Dati del form non validi.'})
    else:
        form = TavoloBookingForm()
    return render(request, 'core/prenotazione_tavolo.html', {'form': form})