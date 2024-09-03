from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone

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

    tipo = models.CharField(max_length=10, choices=ROOM_SIZE_CHOICES)
    camere_totali = models.IntegerField(default=0)  # Numero totale di camere di questo tipo
    nome = models.CharField(max_length=50)
    numero_posti_letto = models.IntegerField(default=1)
    prezzo_per_notte = models.DecimalField(max_digits=10, decimal_places=2)  # Prezzo per notte
    descrizione = models.TextField(blank=True)
    MY_CONSTANT = "camere/"
    immagine1 = models.ImageField(upload_to= MY_CONSTANT, blank=True, null=True)
    immagine2 = models.ImageField(upload_to= MY_CONSTANT, blank=True, null=True)
    immagine3 = models.ImageField(upload_to= MY_CONSTANT, blank=True, null=True)

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
    
    class Meta:
        verbose_name = "Camera"
        verbose_name_plural = "Camere"


class Tavolo(models.Model):
    numero = models.IntegerField(unique=True)
    posti = models.IntegerField()

    def __str__(self):
        return f"Tavolo {self.numero} - {self.posti} posti"

    class Meta:
        verbose_name = "Tavolo"
        verbose_name_plural = "Tavoli"

class TavoloBooking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tavolo = models.ForeignKey(Tavolo, on_delete=models.CASCADE)
    data = models.DateField()
    orario_arrivo = models.TimeField()
    tipo_pasto = models.CharField(choices=[('pranzo', 'Pranzo'), ('cena', 'Cena')], max_length=15)
    numero_persone = models.IntegerField()
    numero_telefono = models.CharField(max_length=15)
    email = models.EmailField(max_length=254)
    note = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.tavolo} - {self.data} - {self.tipo_pasto}"
    
    class Meta:
        verbose_name = "Prenotazione Tavolo"
        verbose_name_plural = "Prenotazioni Tavoli"
        ordering = ['data']  # Ordina le prenotazioni per data in modo crescente

class MenuItem(models.Model):
    CATEGORIE = [
        ('antipasti', 'Antipasti'),
        ('primi', 'Primi'),
        ('secondi', 'Secondi'),
        ('contorni', 'Contorni'),
        ('dolci', 'Dolci'),
        ('bevande', 'Bevande'),
    ]

    nome = models.CharField(max_length=100, unique=True)
    descrizione = models.TextField()
    prezzo = models.DecimalField(max_digits=5, decimal_places=2)
    categoria = models.CharField(max_length=20, choices=CATEGORIE)
    immagine = models.ImageField(upload_to='menu/', blank=True, null=True)

    def __str__(self):
        return self.nome
       
    class Meta:
        verbose_name = "Articolo del Menu"
        verbose_name_plural = "Articoli del Menu"


class Recensione(models.Model):
    CATEGORIE = [
        ('ristorante', 'Ristorante'),
        ('albergo', 'Albergo'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    voto = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    commento = models.TextField()
    immagine = models.ImageField(upload_to='review_images/', null=True, blank=True)
    categoria = models.CharField(max_length=20, choices=CATEGORIE)
    data = models.DateField(default=timezone.now) 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Recensione di {self.user.username}"

        
    def save(self, *args, **kwargs):
       self.clean()  # Esegue la pulizia (e il controllo) prima di salvare
       super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = "Recensione"
        verbose_name_plural = "Recensioni"



class RoomBooking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE)  # Associazione corretta alla classe Camera
    start_date = models.DateField()
    end_date = models.DateField()
    numero_telefono = models.CharField(max_length=15)
    email = models.EmailField()
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def notti_soggiorno(self):
        return (self.end_date - self.start_date).days
    

    def __str__(self):
        return f"Prenotazione di {self.user.username} per {self.camera.get_tipo_display()}"

    class Meta:
        verbose_name = "Prenotazione Camera"
        verbose_name_plural = "Prenotazioni Camere"
        ordering = ['start_date']