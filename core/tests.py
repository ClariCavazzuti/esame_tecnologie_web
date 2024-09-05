from django.test import TestCase
from .models import Camera, RoomBooking, Recensione, Tavolo, TavoloBooking
from django.contrib.auth.models import User
from datetime import date
from .forms import RecensioneForm
from django.urls import reverse
from django.test import Client
from django.conf import settings

class CameraModelTestCase(TestCase):
    def setUp(self):
        self.camera = Camera.objects.create(
            nome="Camera Deluxe",
            tipo="large",
            camere_totali=5,
            numero_posti_letto=2,
            prezzo_per_notte=120.00
        )

    def test_camera_creation_with_correct_attributes(self):
        """Testa la corretta creazione di una Camera con i suoi attributi."""
        self.assertEqual(self.camera.nome, "Camera Deluxe")
        self.assertEqual(self.camera.camere_totali, 5)

class RoomBookingModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.camera = Camera.objects.create(
            nome="Camera Deluxe",
            tipo="large",
            camere_totali=5,
            numero_posti_letto=2,
            prezzo_per_notte=120.00
        )

    def test_room_booking_creation(self):
        """Testa la corretta creazione di una prenotazione di una camera."""
        prenotazione = RoomBooking.objects.create(
            user=self.user,
            camera=self.camera,
            start_date=date.today(),
            end_date=date.today()
        )
        self.assertEqual(prenotazione.camera.nome, "Camera Deluxe")
        self.assertEqual(prenotazione.notti_soggiorno, 0)

class RecensioneModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_recensione_creation_with_valid_attributes(self):
        """Testa la corretta creazione di una Recensione con attributi validi."""
        recensione = Recensione.objects.create(
            user=self.user,
            voto=5,
            commento="Eccellente",
            categoria="albergo",
            data=date.today()
        )
        self.assertEqual(recensione.voto, 5)
        self.assertEqual(recensione.commento, "Eccellente")


class RecensioneFormTestCase(TestCase):
    def test_review_form_does_not_allow_future_date(self):
        """Testa che il form di Recensione non accetti una data futura."""
        data_futura = {
            'voto': 5,
            'commento': 'Ottimo',
            'categoria': 'albergo',
            'data': date.today().replace(year=date.today().year + 1)
        }
        form = RecensioneForm(data=data_futura)
        self.assertFalse(form.is_valid())
        self.assertIn('Non puoi inserire una data futura per la recensione.', form.errors['data'])


class ViewAccessTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_protected_view_accessible_when_logged_in(self):
        """Testa che un utente autenticato possa accedere alla view 'aggiungi_recensione'."""
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('aggiungi_recensione'))
        self.assertEqual(response.status_code, 200)

    def test_protected_view_redirects_to_login_when_not_logged_in(self):
        """Testa che un utente non autenticato venga rediretto al login."""
        response = self.client.get(reverse('aggiungi_recensione'))
        self.assertEqual(response.status_code, 302)


class HomePageContentTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_page_contains_expected_content(self):
        """Testa che la home page contenga il contenuto atteso."""
        response = self.client.get(reverse('core_home'))
        self.assertContains(response, 'Benvenuti al Ristorante Albergo Kristall')
        self.assertContains(response, 'Contattaci')


class RecensioneAPITestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

    def test_api_allows_review_submission(self):
        """Testa che l'API permetta l'invio di una recensione valida."""
        response = self.client.post(reverse('aggiungi_recensione'), {
            'voto': 5,
            'commento': 'Ottimo',
            'categoria': 'albergo',
            'data': date.today(),
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)


class TavoloBookingTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        self.tavolo = Tavolo.objects.create(numero=1, posti=4)

    def test_tavolo_booking_creation(self):
        """Testa la corretta creazione di una prenotazione di un tavolo."""
        prenotazione = TavoloBooking.objects.create(
            user=self.user,
            tavolo=self.tavolo,
            data=date.today(),
            orario_arrivo='12:00',
            tipo_pasto='pranzo',
            numero_persone=2,
            numero_telefono='1234567890',
            note='Test note'
        )
        self.assertEqual(prenotazione.user.username, 'testuser')
        self.assertEqual(prenotazione.tavolo.numero, 1)
        self.assertEqual(prenotazione.numero_persone, 2)
        self.assertEqual(str(prenotazione), f"{prenotazione.user.username} - Tavolo {prenotazione.tavolo.numero} - {prenotazione.tavolo.posti} posti - {prenotazione.data} - {prenotazione.tipo_pasto}")


class EliminaPrenotazioneCameraTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        self.camera = Camera.objects.create(
            nome="Camera Deluxe",
            tipo="large",
            camere_totali=5,
            numero_posti_letto=2,
            prezzo_per_notte=120.00
        )
        self.prenotazione = RoomBooking.objects.create(
            user=self.user,
            camera=self.camera,
            start_date=date.today(),
            end_date=date.today()
        )

    def test_eliminazione_prenotazione_camera(self):
        """Testa che un utente autenticato possa eliminare una prenotazione di camera."""
        response = self.client.post(reverse('elimina_prenotazione_camera', args=[self.prenotazione.id]))
        self.assertRedirects(response, reverse('area_personale'))
        self.assertFalse(RoomBooking.objects.filter(id=self.prenotazione.id).exists())




class EliminaPrenotazioneTavoloTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        self.tavolo = Tavolo.objects.create(numero=1, posti=4)
        self.prenotazione = TavoloBooking.objects.create(
            user=self.user,
            tavolo=self.tavolo,
            data=date.today(),
            orario_arrivo='12:00',
            tipo_pasto='pranzo',
            numero_persone=2,
            numero_telefono='1234567890',
            note='Test note'
        )

    def test_eliminazione_prenotazione_tavolo(self):
        """Testa che un utente autenticato possa eliminare una prenotazione di tavolo."""
        response = self.client.post(reverse('elimina_prenotazione_tavolo', args=[self.prenotazione.id]))
        self.assertRedirects(response, reverse('area_personale'))
        self.assertFalse(TavoloBooking.objects.filter(id=self.prenotazione.id).exists())



class EliminaRecensioneTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        self.recensione = Recensione.objects.create(
            user=self.user,
            voto=5,
            commento="Eccellente",
            categoria="albergo",
            data=date.today()
        )

    def test_eliminazione_recensione(self):
        """Testa che un utente autenticato possa eliminare una recensione."""
        response = self.client.post(reverse('elimina_recensione', args=[self.recensione.id]))
        self.assertRedirects(response, reverse('area_personale'))
        self.assertFalse(Recensione.objects.filter(id=self.recensione.id).exists())

