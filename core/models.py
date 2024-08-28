from django.db import models
from django.contrib.auth.models import User

class Core(models.Model):
    campo1 = models.CharField(max_length=100)
    campo2 = models.TextField()

    def __str__(self):
        return self.campo1


class Camera(models.Model):
    SMALL = 'small'
    MEDIUM = 'medium'
    LARGE = 'large'

    ROOM_SIZE_CHOICES = [
        (SMALL, 'Piccola'),
        (MEDIUM, 'Media'),
        (LARGE, 'Grande'),
    ]

    tipo = models.CharField(max_length=10, choices=ROOM_SIZE_CHOICES, unique=True)
    camere_totali = models.IntegerField(default=0)  # Numero totale di camere di questo tipo
    nome = models.CharField(max_length=50)
    numero_posti_letto = models.IntegerField(default=1)
    prezzo_per_notte = models.DecimalField(max_digits=10, decimal_places=2)  # Prezzo per notte
    descrizione = models.TextField(blank=True, null=True)
    immagine1 = models.ImageField(upload_to='camere/', blank=True, null=True)
    immagine2 = models.ImageField(upload_to='camere/', blank=True, null=True)
    immagine3 = models.ImageField(upload_to='camere/', blank=True, null=True)

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.numero_posti_letto} posti letto - {self.prezzo_per_notte}€/notte"
    
    def decrementa_camere_disponibili(self, start_date, end_date):
        bookings_in_range = RoomBooking.objects.filter(
            camera=self,
            start_date__lt=end_date,
            end_date__gt=start_date
        ).count()
        
        if bookings_in_range < self.camere_totali:
            return True
        return False

    def incrementa_camere_disponibili(self):
        self.camere_totali += 1
        self.save()
    
    class Meta:
        verbose_name = "Camera"
        verbose_name_plural = "Camere"


class Tavolo(models.Model):
    numero = models.IntegerField()
    posti = models.IntegerField()
    disponibile = models.BooleanField(default=True)

    def __str__(self):
        return f"Tavolo {self.numero} - {self.posti} posti"

    class Meta:
        verbose_name = "Tavolo"
        verbose_name_plural = "Tavoli"

class MenuItem(models.Model):
    CATEGORIE = [
        ('antipasti', 'Antipasti'),
        ('primi', 'Primi'),
        ('secondi', 'Secondi'),
        ('contorni', 'Contorni'),
        ('dolci', 'Dolci'),
        ('bevande', 'Bevande'),
    ]

    nome = models.CharField(max_length=100)
    descrizione = models.TextField()
    prezzo = models.DecimalField(max_digits=5, decimal_places=2)
    categoria = models.CharField(max_length=20, choices=CATEGORIE)
    immagine = models.ImageField(upload_to='menu/', blank=True, null=True)

    def __str__(self):
        return self.nome


class Recensione(models.Model):
    utente = models.ForeignKey(User, on_delete=models.CASCADE)
    voto = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    commento = models.TextField()
    immagine = models.ImageField(upload_to='review_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Recensione di {self.utente.username}"


class RoomBooking(models.Model):
    utente = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE)  # Associazione corretta alla classe Camera
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prenotazione di {self.utente.username} per {self.camera.get_tipo_display()}"

    class Meta:
        verbose_name = "Prenotazione"
        verbose_name_plural = "Prenotazioni"