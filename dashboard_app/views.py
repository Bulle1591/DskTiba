from django.views.generic import TemplateView


class DashboardView(TemplateView):
    template_name = 'dashboard_app/index.html'