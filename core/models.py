from django.db import models
from django.contrib.auth.models import User

class Core(models.Model):
    campo1 = models.CharField(max_length=100)
    campo2 = models.TextField()

    def __str__(self):
        return self.campo1

class Camera(models.Model):
    nome = models.CharField(max_length=50)
    numero_posti_letto = models.IntegerField()
    disponibile = models.BooleanField(default=True)
    prezzo_per_notte = models.FloatField()
    descrizione = models.TextField(blank=True, null=True)
    immagini = models.ImageField(upload_to='camere/', blank=True, null=True)

    def __str__(self):
        return f"{self.nome} - {self.numero_posti_letto} posti letto"

class PrenotazioneCamera(models.Model):
    utente = models.ForeignKey(User, on_delete=models.CASCADE)
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE)
    data_inizio = models.DateField()
    data_fine = models.DateField()

    def __str__(self):
        return f"Prenotazione per {self.utente} - Camera: {self.camera}"

class Tavolo(models.Model):
    numero = models.IntegerField()
    posti = models.IntegerField()
    disponibile = models.BooleanField(default=True)

    def __str__(self):
        return f"Tavolo {self.numero} - {self.posti} posti"

class PrenotazioneTavolo(models.Model):
    utente = models.ForeignKey(User, on_delete=models.CASCADE)
    tavolo = models.ForeignKey(Tavolo, on_delete=models.CASCADE)
    data_prenotazione = models.DateTimeField()

    def __str__(self):
        return f"Prenotazione Tavolo {self.tavolo.numero} per {self.utente}"

class MenuItem(models.Model):
    nome = models.CharField(max_length=100)
    descrizione = models.TextField()
    prezzo = models.DecimalField(max_digits=5, decimal_places=2)
    immagine = models.ImageField(upload_to='menu/', blank=True, null=True)

    def __str__(self):
        return self.nome

class Recensione(models.Model):
    utente = models.ForeignKey(User, on_delete=models.CASCADE)
    testo = models.TextField()
    valutazione = models.IntegerField()
    immagini = models.ImageField(upload_to='recensioni/', blank=True, null=True)
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Recensione di {self.utente} - {self.valutazione} stelle"
