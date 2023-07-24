from django.urls import path

from gpt_reservation_system.appointments.views import GPTManageAppointmentView

app_name = "appointments"
urlpatterns = [
    path("manage/", view=GPTManageAppointmentView.as_view(), name="manage"),
]
