import json
from datetime import datetime
from typing import Dict, Optional

import pytz
import requests
from django.conf import settings

from gpt_reservation_system.appointments.exceptions import AppointmentException

# GPT parameters
MAX_TOKENS = 300
PATCH_MAX_LENGTH = 5500
TEMPERATURE = 0.8

# Timezone
LOCAL_TIMEZONE = pytz.timezone("Europe/Istanbul")
LOCAL_TIME = datetime.now(LOCAL_TIMEZONE).isoformat()

# Prompts
SYSTEM_PROMPT = f"""
You're a native Turkish speaker assistant within the GMT+3 timezone who helps businesses manage appointment
requests coming from clients. You will be given a appointment request as a Turkish sentence and you should find out
for which datetime the appointment was requested and the intent of the request.
Only return the intent string and the GMT+3 datetime as a ISO 8601 string in JSON format.
Example format for the JSON is {{\"intent\": \"new_appointment\", \"datetime\": \"2023-07-24T15:45:00+03:00\"}}.
The available values for the `intent` are `new_appointment` and `other`, where `new_appointment` indicates that a
new appointment request has been made and `other` is for other requests, such as when a client wants to cancel an
already existing appointment. The current date and time is "
"""


class AppointmentManager:
    def __init__(self):
        self.system_prompt = SYSTEM_PROMPT
        self.local_time = datetime.now(LOCAL_TIMEZONE).isoformat()

        OPENAI_API = requests.Session()
        OPENAI_API.headers.update(
            {"Content-Type": "application/json", "Authorization": f"Bearer {settings.OPENAI_TOKEN}"}
        )
        self.openai_api = OPENAI_API
        self.openai_model = settings.OPENAI_MODEL

    def execute(self, user_prompt: str) -> Optional[Dict]:
        """Gets appointment intent and date time given a Turkish sentence user prompt.

        Raises:
            AppointmentException: When there is an error during the request / response cycle.
        """

        try:
            return self.get_appointment_details(user_prompt)
        except AppointmentException as e:
            raise e

    def get_appointment_details(self, user_prompt: str) -> Dict:
        """Gets appointment intent and date time given a Turkish sentence user prompt.

        Raises:
            AppointmentException: When there is an error during the request / response cycle.
        """

        try:
            response = self.openai_api.post(
                "https://api.openai.com/v1/chat/completions",
                json={
                    "model": self.openai_model,
                    "messages": [
                        {"role": "system", "content": self.system_prompt + self.local_time},
                        {"role": "user", "content": f"{user_prompt}"},
                    ],
                    "n": 1,
                    "temperature": TEMPERATURE,
                    "max_tokens": MAX_TOKENS,
                },
            )
            gpt_json_str = response.json()["choices"][0]["message"]["content"].strip()
            return json.loads(gpt_json_str)
        except Exception as e:
            raise AppointmentException(f"Error occurred during appointment extraction. Error: {e.__str__()}")
