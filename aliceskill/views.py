from __future__ import unicode_literals

# Импортируем модули для работы с JSON и логами.
import json
import logging
from django.views.decorators.csrf import csrf_exempt


sessionStorage = {}


logging.basicConfig(level=logging.DEBUG)

@csrf_exempt
def main(request):
# Функция получает тело запроса и возвращает ответ.
    body = json.loads(request.body)
    logging.info('Request: %r', body)

    response = {
        "version": body['version'],
        "session": body['session'],
        "response": {
            "end_session": False
        }
    }
    return {
  "response": {
    "text": "Здравствуйте! Это мы, хороводоведы.",
    "tts": "Здравствуйте! Это мы, хоров+одо в+еды.",
    "buttons": [
        {
            "title": "Надпись на кнопке",
            "payload": {},
            "url": "https://example.com/",
            "hide": true
        }
    ],
    "end_session": false
  },
  "version": "1.0"
}