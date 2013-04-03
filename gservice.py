from flask import redirect, render_template, request
from service import HomeView, LookupView, ManageView, Service

class GHomeView(HomeView):
    template_name = 'g/home.html'

class GLookupView(LookupView):
    def lookup(self, identifier):
        # Hardcodes /about to itself.
        if identifier == 'about':
            return 'http://g/'
        return None

class GManageView(ManageView):
    template_name = 'g/manage.html'

    def generate_identifier():
        # TODO: generate unique identifier
        return ""

    def is_taken(identifier):
        # TODO: check if identifier is taken
        return False

    def create_short_link(identifier, url):
        # TODO: save short link

    def post(self):
        url = request.form.get('url', None)
        if not url:
            error = "Please enter a URL."
            return render_template(self.template_name, error=error)

        # Ensure URL starts with http:// or https://
        if not (url.startswith("http://") or url.startswith("https://"):
            url = 'http://' + url

        identifier = request.form.get('identifier', None)
        if identifier:
            # Check if identifier is taken
            if is_taken(identifier):
                error = "%s is taken - please try another one." % identifier
                return render_template(self.template_name, error=error)
        else:
            # Generate a unique identifier
            identifier = generate_identifier()

        create_short_link(identifier, url)
        return redirect(identifier)

class GService(Service):
    home = GHomeView
    lookup = GLookupView
    manage = GManageView
