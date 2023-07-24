from django.conf import settings
from django.urls import include, path

urlpatterns = [
    # Appointment management
    path("appointments/", include("gpt_reservation_system.appointments.urls", namespace="users")),
]


if settings.DEBUG:
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
