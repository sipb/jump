from service import HomeView, LookupView, ManageView, Service

class GHomeView(HomeView):
    template_name = "g/home.html"

class GLookupView(LookupView):
    pass

class GManageView(ManageView):
    template_name = "g/manage.html"

class GService(Service):
    home = GHomeView
    lookup = GLookupView
    manage = GManageView
