from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "gpt_reservation_system.appointments"
    verbose_name = _("Users")

    def ready(self):
        try:
            import gpt_reservation_system.appointments.signals  # noqa: F401
        except ImportError:
            pass
