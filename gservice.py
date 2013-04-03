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

class GService(Service):
    home = GHomeView
    lookup = GLookupView
    manage = GManageView
