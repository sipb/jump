import os
from urlparse import urlparse

from flask import current_app, redirect, render_template, request
from flask.views import MethodView

class HomeView(MethodView):
    """Renders a home page for the service.

    Override template_name to render custom template.
    """
    template_name = 'default_home.html'

    def get(self):
        return render_template(self.template_name)

class LookupView(MethodView):
    """Core URL expansion view, generates redirects.

    Override lookup to return URL identifier maps to, or None if non-existent.
    """

    def lookup(self, identifier):
        return None
    
    def get(self, path):
        """ Generates redirect to expanded URL.

        Assumes path is in the format
            identifier
        or
            identifier/optional/appended/path,

        which expands to
            lookup(identifier)
        or
            lookup(identifier)/optional/appended/path
        """
        identifier, sep, appended_path = path.partition('/')
        lookup_url = self.lookup(identifier)
        if not lookup_url:
            return render_template('404.html'), 404

        # It's important that we use `sep`, which might be an empty string if
        # there's no slash in path.
        redirect_url = "%s%s%s" % (lookup_url, sep, appended_path)
        return redirect(redirect_url)

class ManageView(MethodView):
    """Provides view to make any data changes.

    All potentially dangerous operations should be done through the manage
    view. By default, forces https. Set envvar HTTPS=false to disable.

    Override template_name to render custom template.
    Override post to process any POST-ed data.
    """
    template_name = 'default_manage.html'

    def post(self):
        return redirect(request.path)

    def get(self):
        disable_https = (os.environ.get('HTTPS', 'true') == 'false')
        if (not disable_https) and request.url.startswith('http://'):
            parsed_url = urlparse(request.url)
            secure_url = "https://%s:444%s" % (parsed_url.hostname, parsed_url.path)
            return redirect(secure_url, 302)
        return render_template(self.template_name)

class Service:
    home = HomeView
    lookup = LookupView
    manage = ManageView

    def home_view(self):
        return self.home.as_view('home')

    def lookup_view(self):
        return self.lookup.as_view('lookup')

    def manage_view(self):
        return self.manage.as_view('manage')
