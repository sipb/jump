from flask import Flask
from service import Service
from gservice import GService

app = Flask(__name__)

class ServiceDirectory:

    def __init__(self):
        self.services = {}

    def register(self, service_name, service):
        """Registers a link-shortener service.

        service_name -- hostname to match on, e.g. "g" for g.mit.edu
        service -- actual Service object
        """
        assert isinstance(service, Service), "service must be Service class"
        self.services[service_name] = service

    def config_app(self, app):
        for service_name, service in self.services.items():
            base_url = '/%s/' % service_name
            print "registering %s" % base_url
            app.add_url_rule(base_url, view_func=service.home_view())
            app.add_url_rule(base_url + '<path>', view_func=service.lookup_view())
            app.add_url_rule(base_url + 'manage/', view_func=service.manage_view())

s = ServiceDirectory()
s.register('g', GService())
s.config_app(app)

if __name__ == "__main__":
    app.run(debug=True)
