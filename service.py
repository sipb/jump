from flask import render_template
from flask.views import View

class HomeView(View):
    methods = ['GET']
    template_name = "default_home.html"

    def dispatch_request(self):
        return render_template(self.template_name)

class LookupView(View):
    methods = ['GET']
    
    def dispatch_request(self, path):
        return render_template("404.html"), 404

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
