from typing import Any
from django import forms
from .models import RoomBooking, TavoloBooking, Recensione
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from datetime import time

class RoomSearchForm(forms.Form):
    """
    Form per cercare camere disponibili basato su date e numero di posti letto.
    """
    check_in_date = forms.DateField(label='Data di inizio', widget=forms.DateInput(attrs={'type': 'date'}))
    check_out_date = forms.DateField(label='Data di fine', widget=forms.DateInput(attrs={'type': 'date'}))
    posti_letto = forms.IntegerField(label='Numero di posti letto', min_value=1)

class RoomBookingForm(forms.ModelForm):
    class Meta:
        model = RoomBooking
        fields = ['start_date', 'end_date', 'numero_telefono', 'note']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'note': forms.Textarea(attrs={'rows': 3}),
        }

    def clean(self):
        """
        Validazione del form per assicurarsi che la data di fine sia successiva alla data di inizio.
        """
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if start_date and end_date and start_date >= end_date:
            raise forms.ValidationError("La data di fine deve essere successiva alla data di inizio.")

        return cleaned_data


class TavoloBookingForm(forms.ModelForm):
    ORARI_DISPONIBILI = [
        ('12:00', '12:00'),
        ('12:30', '12:30'),
        ('13:00', '13:00'),
        ('13:30', '13:30'),
        ('14:00', '14:00'),
        ('14:30', '14:30'),
        ('15:00', '15:00'),
        ('19:30', '19:30'),
        ('20:00', '20:00'),
        ('20:30', '20:30'),
        ('21:00', '21:00'),
        ('21:30', '21:30'),
        ('22:00', '22:00'),
    ]
    
    orario_arrivo = forms.ChoiceField(choices=ORARI_DISPONIBILI)
    
    class Meta:
        model = TavoloBooking
        fields = ['data', 'orario_arrivo', 'tipo_pasto', 'numero_persone', 'numero_telefono', 'note']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        orario = cleaned_data.get('orario_arrivo')
        tipo_pasto = cleaned_data.get('tipo_pasto')

        if orario and tipo_pasto:
            orario_time = time.fromisoformat(orario)
            
            if time(12, 0) <= orario_time <= time(15, 0) and tipo_pasto != 'pranzo':
                self.add_error('tipo_pasto', "Seleziona 'Pranzo' per l'orario compreso tra le 12:00 e le 15:00.")
            elif time(19, 30) <= orario_time <= time(22, 0) and tipo_pasto != 'cena':
                self.add_error('tipo_pasto', "Seleziona 'Cena' per l'orario compreso tra le 19:30 e le 22:00.")
        
        return cleaned_data


class RecensioneForm(forms.ModelForm):
    class Meta:
        model = Recensione
        fields = ['voto', 'commento', 'immagine', 'categoria', 'data']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}),
        }


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Obbligatorio. Inserisci un indirizzo email valido.")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
