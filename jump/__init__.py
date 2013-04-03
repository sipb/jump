<<<<<<< HEAD
from flask import Flask, render_template, request
=======
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
>>>>>>> Adds database backing for g/ to save and query redirects

from util import require_env

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = require_env('DB_URI')
db = SQLAlchemy(app)

from service import Service
from g.gservice import GService

def register(app, services):
    """Adds the sets of URLs for each service on the app.
    Each service with service_name is added with
        /service_name/ -- home page
        /service_name/manage -- manage page
        /service_name/<path> -- catch all page for redirecting URLs
    """
    for service_name, service in services.items():
        base_url = '/%s/' % service_name
        print "registering %s" % base_url
        app.add_url_rule(base_url, view_func=service.home_view())
        app.add_url_rule(base_url + 'manage/', view_func=service.manage_view())
        app.add_url_rule(base_url + '<path>', view_func=service.lookup_view())

def init_db():
    from g.models import GRedirect
    db.create_all()

services = {
    'g': GService(),
}
register(app, services)

@app.route('/')
def main():
    return render_template('main.html', services=services)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
