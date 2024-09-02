# middleware.py

from datetime import timedelta, datetime
from django.conf import settings
from django.shortcuts import redirect
from django.utils.timezone import now
from django.utils.deprecation import MiddlewareMixin

class AutoLogoutMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not request.user.is_authenticated:
            return

        # Verifica se l'utente è attivo o meno
        session_expiry = request.session.get('session_expiry')

        if session_expiry:
            session_expiry = datetime.fromisoformat(session_expiry)
            if session_expiry < now():
                # Cancella la sessione e reindirizza alla pagina di logout inattivo
                del request.session['session_expiry']
                return redirect('inactive_logout')

        # Aggiorna il timer di scadenza della sessione
        request.session['session_expiry'] = (now() + timedelta(seconds=settings.SESSION_COOKIE_AGE)).isoformat()

