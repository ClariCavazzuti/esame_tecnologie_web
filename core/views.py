from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import MenuItem, Camera, RoomBooking, TavoloBooking, Tavolo, Recensione
from .forms import RoomSearchForm, RoomBookingForm, TavoloBookingForm, RecensioneForm
from django.http import JsonResponse
from datetime import datetime
from django.contrib import messages 



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
    # Prendi il parametro di ordinamento dalla richiesta GET, di default ordina per data
    ordine = request.GET.get('ordine', 'data')
    
    # Filtra le recensioni per categoria e ordina secondo il parametro scelto
    recensioni_ristorante = Recensione.objects.filter(categoria='ristorante').order_by(ordine)
    recensioni_albergo = Recensione.objects.filter(categoria='albergo').order_by(ordine)
    
    context = {
        'recensioni': {
            'ristorante': recensioni_ristorante,
            'albergo': recensioni_albergo,
        },
        'ordine_corrente': ordine,  # Aggiungi il parametro di ordinamento corrente al contesto
    }
    
    return render(request, 'core/recensioni.html', context)



@login_required
def aggiungi_recensione(request):
    if request.method == 'POST':
        form = RecensioneForm(request.POST, request.FILES)
        if form.is_valid():
            recensione = form.save(commit=False)
            recensione.user = request.user
            recensione.save()
            return JsonResponse({'success': True, 'message': 'Recensione caricata con successo!'}, status=200)
        else:
            return JsonResponse({'success': False, 'message': 'Errore nel caricamento della recensione. Controlla i dati inseriti.'}, status=400)
    else:
        form = RecensioneForm()
    return render(request, 'core/aggiungi_recensione.html', {'form': form})



@login_required
def elimina_recensione(request, recensione_id):
    recensione = get_object_or_404(Recensione, id=recensione_id, user=request.user)
    recensione.delete()
    messages.success(request, 'Recensione eliminata con successo')
    return redirect('area_personale')




def camere(request):
    camere = Camera.objects.all()
    return render(request, 'core/pagina-camere.html', {'camere': camere})



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

        
            available_rooms = [camera for camera in available_rooms if check_availability(camera, check_in_date, check_out_date)]

            if not available_rooms:
                messages.error(request, 'Nessuna camera disponibile per le date e il numero di posti letto selezionati.')
            else:
                
                return render(request, 'core/room_search_results.html', {
                    'available_rooms': available_rooms,
                    'check_in_date': check_in_date,
                    'check_out_date': check_out_date,
                })

    else:
        form = RoomSearchForm()
    return render(request, 'core/search_rooms.html', {'form': form})




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



@login_required
def confirm_booking(request):
    if request.method == 'POST':
        selected_room_ids = request.POST.getlist('camere')
        check_in_date = request.POST.get('check_in_date')
        check_out_date = request.POST.get('check_out_date')
        numero_telefono = request.POST.get('numero_telefono')
        note = request.POST.get('note')

        
        try:
            check_in_date = datetime.strptime(check_in_date, '%Y-%m-%d').date()
            check_out_date = datetime.strptime(check_out_date, '%Y-%m-%d').date()
        except ValueError:
            messages.error(request, 'Il formato della data non è valido.')
            return redirect('search_rooms')
        
        if not selected_room_ids:
            messages.error(request, 'Seleziona almeno una camera per procedere con la prenotazione.')
            return redirect('search_rooms')

        
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




def booking_success(request):
    last_booking = RoomBooking.objects.filter(user=request.user).order_by('-created_at').first()
    return render(request, 'core/booking_success.html', {'booking': last_booking})




@login_required
def elimina_prenotazione_camera(request, prenotazione_id):
    prenotazione = get_object_or_404(RoomBooking, id=prenotazione_id, user=request.user)
    camera = prenotazione.camera
    prenotazione.delete()
    messages.success(request, f"La prenotazione della camera {camera.nome} è stata eliminata con successo.")
    return redirect('area_personale')



def tavoli(request):
    return render(request,'core/tavoli.html')



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



@login_required
def elimina_prenotazione_tavolo(request, prenotazione_id):
    prenotazione = get_object_or_404(TavoloBooking, id=prenotazione_id, user=request.user)
    tavolo = prenotazione.tavolo
    prenotazione.delete()
    messages.success(request, f"La prenotazione del tavolo numero {tavolo.numero} è stata eliminata con successo.")
    return redirect('area_personale')




@login_required
def area_personale(request):
    # Recupera le prenotazioni camere, tavoli e recensioni dell'utente
    prenotazioni_camere = RoomBooking.objects.filter(user=request.user)
    prenotazioni_tavoli = TavoloBooking.objects.filter(user=request.user)
    recensioni = Recensione.objects.filter(user=request.user)

    context = {
        'prenotazioni_camere': prenotazioni_camere,
        'prenotazioni_tavoli': prenotazioni_tavoli,
        'recensioni': recensioni,
    }
    
    return render(request, 'core/area_personale.html', context)






