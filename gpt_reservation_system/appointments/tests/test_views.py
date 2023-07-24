from datetime import datetime

import pytest
from django.urls import reverse
from freezegun import freeze_time
from rest_framework.test import APIClient


class TestGPTManageAppointmentView:
    manage_url = reverse("appointments:manage")

    def send_manage_request(self, user_prompt):
        response = APIClient().post(self.manage_url, {"user_prompt": user_prompt}, format="json")
        return response

    @pytest.mark.parametrize(
        "user_prompt,intent,expected_date_time",
        [
            ("Yarin oglen 2'de musait misiniz?", "new_appointment", "2023-07-25T14:00:00+03:00"),
            ("Haftaya 16:30'a rezervasyon yapabilir miyiz?", "new_appointment", "2023-07-31T16:30:00+03:00"),
            ("Bugunku rezervasyonumuzu iptal edelim.", "other", "2023-07-24T16:00:00+03:00"),
            ("Bu Carsamba 2'ye ceyrek kalaya ayarlayalim mi?", "new_appointment", "2023-07-26T13:45:00+03:00"),
            ("28 Temmuz'daki rezervasyonumuzu saat 17'ye degistirebilir miyiz?", "other", "2023-07-28T17:00:00+03:00"),
        ],
    )
    def test_manage_view(self, user_prompt, intent, expected_date_time):
        # Given
        current_utc_time = datetime(2023, 7, 24, 13, 0, 0)
        # When
        with freeze_time(current_utc_time):
            response = self.send_manage_request(user_prompt)
        # Then
        json_response = response.json()
        assert json_response["is_success"] is True
        assert json_response["intent"] == intent
        assert json_response["datetime"] == expected_date_time
