from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from telegram_connect.models import Profile


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "profile/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = Profile.objects.filter(user=self.request.user)[0]
        return context
