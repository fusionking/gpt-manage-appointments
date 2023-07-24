from rest_framework.response import Response
from rest_framework.views import APIView

from gpt_reservation_system.appointments.serializers import GPTManageAppointmentSerializer


class GPTManageAppointmentView(APIView):
    throttle_scope = "auth"

    serializer_class = GPTManageAppointmentSerializer

    def post(self, request):
        serializer = self.serializer_class(request.data)
        return Response(serializer.data)
