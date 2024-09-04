# Progetto Kristall

Questo è un progetto Django creato per gestire le prenotazioni di camere e tavoli, insieme alla gestione di un menu e recensioni per un ristorante e albergo. Il progetto include funzionalità di autenticazione utente, prenotazione di risorse e gestione del backend tramite l'admin di Django.

## Struttura del Progetto

- **core**: Contiene le app Django principali del progetto.
  - `models.py`: Definisce i modelli per le camere, prenotazioni, tavoli, menu e recensioni.
  - `views.py`: Contiene le viste per la gestione delle prenotazioni, la visualizzazione del menu, e altre pagine principali.
  - `forms.py`: Include i form per la gestione delle prenotazioni e delle recensioni.
  - `urls.py`: Definisce le rotte del progetto.
  - `admin.py`: Configura l'interfaccia di amministrazione di Django per gestire i modelli definiti.

- **progettoesame**: Contiene le configurazioni di base del progetto.
  - `settings.py`: Configurazioni generali del progetto, inclusi i middleware, le app installate e le impostazioni di sicurezza.
  - `urls.py`: Configurazione principale delle URL del progetto.
  - `wsgi.py` e `asgi.py`: Entry point per WSGI/ASGI server.

## Requisiti

Per eseguire questo progetto, assicurati di avere i seguenti requisiti:

- Python 3.8 o successivo
- Django 3.2 o successivo
- `pipenv` o `virtualenv` per gestire l'ambiente virtuale

## Installazione

1. **Clona il repository**:
   ```bash
   git clone https://github.com/tuo-username/progettoesame.git
   cd progettoesame
   ```

2. **Crea un ambiente virtuale e attivalo**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Installa le dipendenze**:
   ```bash
   pip install pipenv
   pip install django-crispy-forms
   pip install crispy-bootstrap4
   ```

4. **Applica le migrazioni**:
   ```bash
   python manage.py migrate
   ```

5. **Crea un superuser per l'amministrazione**:
   ```bash
   python manage.py createsuperuser
   ```

6. **Esegui il server di sviluppo**:
   ```bash
   python manage.py runserver
   ```

## Funzionalità

- **Gestione Camere**: Prenotazione e gestione delle camere disponibili, con riepilogo delle prenotazioni e verifica della disponibilità.
- **Gestione Tavoli**: Prenotazione dei tavoli in base all'orario e al tipo di pasto (pranzo o cena).
- **Recensioni**: Possibilità per gli utenti di lasciare recensioni e visualizzare quelle esistenti.
- **Gestione del Menu**: Visualizzazione degli articoli del menu e gestione tramite l'admin di Django.
- **Interfaccia Admin**: Gestione completa delle risorse tramite l'interfaccia di amministrazione di Django.

## Test

Sono inclusi diversi test unitari per verificare il funzionamento corretto delle funzionalità principali, come la creazione di prenotazioni e la gestione delle recensioni.

Esegui i test con:
```bash
python manage.py test core
```
