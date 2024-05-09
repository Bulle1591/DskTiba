from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class BaseView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'


class DashboardView(BaseView, TemplateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'dashboard_app/index.html'
