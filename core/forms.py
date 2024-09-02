from typing import Any
from django import forms
from .models import RoomBooking, TavoloBooking, Recensione
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


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
    class Meta:
        model = TavoloBooking
        fields = ['data', 'orario_arrivo', 'tipo_pasto', 'numero_persone', 'numero_telefono', 'note']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}),
            'orario_arrivo': forms.TimeInput(format='%H:%M', attrs={'type': 'time'}),
        }

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
