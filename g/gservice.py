from flask import redirect, render_template, request
from jump.service import HomeView, LookupView, ManageView, Service
from models import GRedirect
from jump import db

import random, string

SHORT_NAME_LENGTH = 5
SHORT_NAME_CHARS = string.letters

def generate_short_name():
    return random.sample(SHORT_NAME_CHARS, SHORT_NAME_LENGTH)

def is_taken(short_name):
    return GRedirect.query.filter_by(short_name=short_name).first() is not None

def create_short_link(username, url, short_name):
    g_redirect = GRedirect(username, url, short_name)
    db.session.add(g_redirect)
    db.session.commit()

class GHomeView(HomeView):
    template_name = 'g/home.html'

class GLookupView(LookupView):
    def lookup(self, short_name):
        # Hardcodes /about to itself.
        if short_name == 'about':
            return 'http://g/'
        g_redirect = GRedirect.query.filter_by(short_name=short_name).first()
        if g_redirect is None:
            return None
        return g_redirect.url

class GManageView(ManageView):
    template_name = 'g/manage.html'

    def post(self):
        url = request.form.get('url', None)
        if not url:
            error = "Please enter a URL."
            return render_template(self.template_name, error=error)

        # Ensure URL starts with http:// or https://
        if not (url.startswith("http://") or url.startswith("https://")):
            url = 'http://' + url

        short_name = request.form.get('short_name', None)
        if short_name:
            # Check if short_name is taken
            if is_taken(short_name):
                error = "%s is taken - please try another one." % short_name
                return render_template(self.template_name, error=error)
        else:
            # Generate a unique short_name
            short_name = generate_short_name()

        # TODO(saif): Use username instead of 'lolol'
        create_short_link('lolol', url, short_name)
        return redirect(short_name)

class GService(Service):
    home = GHomeView
    lookup = GLookupView
    manage = GManageView
