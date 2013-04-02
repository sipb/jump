from flask import redirect, render_template
from flask.views import View

class HomeView(View):
    methods = ['GET']
    template_name = "default_home.html"

    def dispatch_request(self):
        return render_template(self.template_name)

class LookupView(View):
    methods = ['GET']

    def lookup(self, identifier):
        return None
    
    def dispatch_request(self, path):
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
            return render_template("404.html"), 404

        # It's important that we use `sep`, which might be an empty string if
        # there's no slash in path.
        redirect_url = "%s%s%s" % (lookup_url, sep, appended_path)
        return redirect(redirect_url, 301)

class ManageView(View):
    methods = ['GET', 'POST']
    template_name = "default_manage.html"

    def dispatch_request(self):
        return render_template(self.template_name)

class Service:
    home = HomeView
    lookup = LookupView
    manage = ManageView

    def home_view(self):
        return self.home.as_view("home")

    def lookup_view(self):
        return self.lookup.as_view("lookup")

    def manage_view(self):
        return self.manage.as_view("manage")
