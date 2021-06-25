import re
from time import time

from captcha.fields import CaptchaField
from django import forms
from django.shortcuts import redirect
from django.views.generic import TemplateView, FormView

from users.models import User


class IndexView(TemplateView):
    template_name = "pages/index.html"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['guest'] = True
        return data


class ContactDoneView(TemplateView):
    template_name = 'pages/kontakt-danke.html'


class ContactForm(forms.Form):
    name = forms.CharField(label_suffix="")
    email = forms.EmailField(label="E-Mail", label_suffix="")
    message = forms.CharField(widget=forms.Textarea, label="Nachricht", label_suffix="")
    captcha = CaptchaField(label_suffix="")


class ContactView(FormView):
    template_name = "pages/kontakt.html"
    form_class = ContactForm
    success_url = '/kontakt-danke'

    def form_valid(self, form):
        user = User.data.get(email="andy@freilandkiwis.de")
        content = {
            'Name': form.cleaned_data['name'],
            'E-Mail': form.cleaned_data['email'],
            'Nachricht': form.cleaned_data['message'],
        }
        user.email_user('kontakt', {'content': content})
        return super().form_valid(form)


def extract_form_data(request_data):
    content = {}

    options = {
        'Anrede': {'1': 'Frau', '2': 'Herr'},
        'Fingerfood': {'1': 'Kalt', '2': 'Kalt-Warm', '3': 'Gabelbissen'},
        'Office Lunch': {'1': 'Kaltes Fingerfood', '2': 'Suppe + Fingerfood', '3': 'Salat + Hauptgang + Dessert'},
        'Buffet': {'1': 'Kalt', '2': 'Warm', '3': 'Kalt-Warm'},
        'Menue': {'1': '3 Gänge', '2': '4 Gänge', '3': '5-6 Gänge'},
        'Speisen': {'1': 'Rustikal / Deutsch', '2': 'Mediterran', '3': 'International'},
        'Budget': {'1': '10,00 - 15,00 Euro', '2': '15,01 - 20,00 Euro', '3': '20,01 - 25,00 Euro', '4': 'ab 25,00 Euro'},
        'Getraenke': {'0': 'nein', '1': 'ja'},
        'Personal': {'0': 'nein', '1': 'ja'},
        'Fingerfood Extra': {'0': 'Schnittchen', '1': 'Canapes', '2': 'Halbes Brötchen'},
        'Speisen Extra': {'0': 'Vegetarisch', '1': 'Bio'},
        'Getraenke Extra': {'0': 'Erfrischungsgetränke', '1': 'Alkoholische Getränke',
                            '2': 'Heißgetränke', '3': 'Bio', '4': 'Fair Trade'},
        'Ausstattung': {'0': 'Geschirr / Besteck', '1': 'Gläser', '2': 'Buffetbereitstellung',
                        '3': 'Tischwäsche', '4': 'Tische / Bestuhlung', '5': 'Blumen',
                        '6': 'Dekoration', '7': 'Zelte'},
        'Zusendung Angebot': {'0': 'E-Mail', '1': 'Post', '2': 'Fax'},
        'Gefunden': {'0': 'Webseite', '1': 'Suchmaschine', '2': 'Empfehlung', '3': 'Kunde / Kundin'}
    }

    labels = {'Zusendung Angebot': 'Ich wünsche die Zusendung des Angebots per',
              'Budget Gesamt': 'Gesamtbudget netto',
              'Budget': 'Budget netto für Speisen pro Person',
              'Email': 'E-Mail',
              'Gefunden': 'Wie sind Sie zu uns gekommen?',
              }

    for key in request_data.keys():
        if key.startswith('data['):
            nice_key = re.sub(r'data\[(.*?)].*', r'\1', key).title()
            nice_key = re.sub('_', ' ', nice_key)
            real_key = labels.get(nice_key, nice_key)
            value = request_data[key]

            if value == '':
                continue

            if value.isdigit() and options.get(nice_key):
                if nice_key not in options:
                    raise ValueError(f'hier fehlen noch Optionen für {nice_key}')

                value = options[nice_key][value]
            if '][' in key and content.get(real_key):
                content[real_key] += f', {value}'
            else:
                content[real_key] = value
    return content


class WorldView(TemplateView):
    template_name = "pages/world.html"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['world'] = True
        return data


class RequestView(TemplateView):
    template_name = "pages/anfrage.html"

    def post(self, request):
        user = User.data.get(email="andy@freilandkiwis.de")
        content = extract_form_data(request.POST)

        # spam detection
        start = int(request.POST['form-nonce'])
        finish = int(time())
        spam = '(SPAM?)' if finish < start + 60 else ''

        user.email_user('anfrage', {'content': content, 'spam': spam})
        return redirect('/jetzt-anfragen-danke')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['anfrage'] = True
        return data


class RequestDoneView(TemplateView):
    template_name = 'pages/anfragen-danke.html'


class PrivacyView(TemplateView):
    template_name = "pages/datenschutz.html"


class ImprintView(TemplateView):
    template_name = "pages/impressum.html"


class TermsView(TemplateView):
    template_name = "pages/agb.html"


class BuffetView(TemplateView):
    template_name = "pages/buffet.html"


class FingerView(TemplateView):
    template_name = "pages/finger.html"


class InspireView(TemplateView):
    template_name = "pages/inspiration.html"


class BioView(TemplateView):
    template_name = "pages/bio.html"


class ServiceView(TemplateView):
    template_name = "pages/service.html"


class DrinksView(TemplateView):
    template_name = "pages/drinks.html"


class LunchView(TemplateView):
    template_name = "pages/lunch.html"


class EventsView(TemplateView):
    template_name = "pages/events.html"
