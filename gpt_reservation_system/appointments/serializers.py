from rest_framework import serializers

from gpt_reservation_system.appointments.exceptions import AppointmentException
from gpt_reservation_system.appointments.manager import AppointmentManager


class GPTManageAppointmentSerializer(serializers.Serializer):
    def to_representation(self, data):
        appointment_manager = AppointmentManager()
        user_prompt = data["user_prompt"]

        try:
            json_response = appointment_manager.execute(user_prompt)
            json_response["is_success"] = True
        except AppointmentException as e:
            json_response = {"error": e.__str__(), "is_success": False}

        return json_response
