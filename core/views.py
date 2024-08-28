from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import MenuItem, Camera, RoomBooking
from .forms import RoomSearchForm, RoomBookingForm

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
            available_rooms = Camera.objects.filter(
                disponibile=True,
                numero_posti_letto__gte=posti_letto,
                roombooking__start_date__gte=check_in_date,
                roombooking__end_date__lte=check_out_date
            ).distinct()
            return render(request, 'core/room_search_results.html', {'available_rooms': available_rooms})
    else:
        form = RoomSearchForm()
    return render(request, 'core/search_rooms.html', {'form': form})