# GPT Reservation System

GPT Reservation System

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

License: MIT

## Using the API

- Make sure to create a `.env` file with the same schema as the `env.example` file and enter your
`OPENAI_TOKEN` to leverage the OPEN AI API.
- Create a new virtualenv with **Python 3.10.8** with the tool of your choice (pyenv, virtualenv etc.) and install the requirements.

    ```bash
    pyenv virtualenv 3.10.8 yourenv &&
    pyenv activate yourenv &&
    pip install -r requirements/local.txt
  ```

- Run `python manage.py runserver` to spin up your server
- Send a `POST` request to `http://localhost:8000/appointments/manage/` via the tool of your choice (curl, POSTMAN etc.)
  - The payload for the request is in this format: `{"user_prompt": "28 Temmuz'daki rezervasyonumuzu saat 17'ye degistirebilir miyiz?"}`
    where the "user_prompt" is the appointment request sentence in Turkish.
- The response should be in this format:
    ```json
      {
        "intent": "other",
        "datetime": "2023-07-28T17:00:00+03:00",
        "is_success": true
      }
  ```
  where "intent" is the appointment intent extracted, "datetime" is the extracted datetime information
  and "is_success" indicates whether the extraction and the I/O operations were successful.

#### Running tests with pytest

    $ pytest

Note that the OPEN AI API is not mocked to test the
actual response, so please be cautious.
