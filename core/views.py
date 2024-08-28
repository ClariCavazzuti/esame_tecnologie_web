from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import MenuItem, Camera, RoomBooking, TavoloBooking
from .forms import RoomSearchForm, RoomBookingForm, TavoloBookingForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import date

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

def camere(request):
    camere = Camera.objects.all()
    return render(request, 'core/pagina-camere.html', {'camere': camere})


    room_types = Camera.objects.all()
    return render(request, 'core/room_details.html', {'room_types': room_types})

@login_required
def book_room(request, camera_id):
    camera = get_object_or_404(Camera, id=camera_id)
    if request.method == 'POST':
        form = RoomBookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.utente = request.user
            booking.camera = camera
            if check_availability(camera, booking.start_date, booking.end_date):
                booking.save()
                return redirect('booking_list')
            else:
                form.add_error(None, 'Camera non disponibile per il periodo selezionato.')
    else:
        form = RoomBookingForm()
    return render(request, 'core/book_room.html', {'form': form, 'camera': camera})

def search_rooms(request):
    if request.method == 'GET':
        form = RoomSearchForm(request.GET)
        if form.is_valid():
            check_in_date = form.cleaned_data['check_in_date']
            check_out_date = form.cleaned_data['check_out_date']
            posti_letto = form.cleaned_data['posti_letto']

            available_rooms = Camera.objects.filter(
                numero_posti_letto__gte=posti_letto
            )

            available_rooms = [camera for camera in available_rooms if check_availability(camera, check_in_date, check_out_date)]

            return render(request, 'core/room_search_results.html', {'available_rooms': available_rooms})
    else:
        form = RoomSearchForm()
    return render(request, 'core/search_rooms.html', {'form': form})

@csrf_exempt
@login_required
def ajax_book_room(request):
    if request.method == 'POST':
        camera_id = request.POST.get('camera_id')
        check_in_date = request.POST.get('check_in_date')
        check_out_date = request.POST.get('check_out_date')
        utente = request.user

        camera = get_object_or_404(Camera, id=camera_id)

        if check_availability(camera, check_in_date, check_out_date):
            RoomBooking.objects.create(
                utente=utente,
                camera=camera,
                start_date=check_in_date,
                end_date=check_out_date
            )
            return JsonResponse({'success': True, 'message': 'Prenotazione effettuata con successo!'})
        else:
            return JsonResponse({'success': False, 'message': 'Camera non disponibile per il periodo selezionato.'})

    return JsonResponse({'success': False, 'message': 'Metodo non consentito'})

@csrf_exempt
@login_required
def ajax_book_rooms(request):
    if request.method == 'POST':
        camera_ids = request.POST.get('camera_ids').split(',')
        check_in_date = request.POST.get('check_in_date')
        check_out_date = request.POST.get('check_out_date')
        utente = request.user

        camere_prenotate = []
        for camera_id in camera_ids:
            camera = get_object_or_404(Camera, id=camera_id)
            if check_availability(camera, check_in_date, check_out_date):
                RoomBooking.objects.create(
                    utente=utente,
                    camera=camera,
                    start_date=check_in_date,
                    end_date=check_out_date
                )
                camere_prenotate.append(camera.nome)
            else:
                return JsonResponse({'success': False, 'message': f'Nessuna camera disponibile per il tipo {camera.nome}'})

        return JsonResponse({'success': True, 'message': 'Prenotazione effettuata con successo per le seguenti camere: ' + ', '.join(camere_prenotate)})

    return JsonResponse({'success': False, 'message': 'Metodo non consentito'})

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
            booking = form.save(commit=False)
            booking.user = request.user
            booking.save()
            messages.success(request, 'Prenotazione effettuata con successo!')
            return redirect('core_home')
    else:
        form = TavoloBookingForm()
    return render(request, 'core/prenotazione_tavolo.html', {'form': form})