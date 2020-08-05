from __future__ import unicode_literals
from django.http import HttpResponse
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
    return HttpResponse( json.dumps({
  "response": {
    "text": "Здравствуйте! Это мы, хороводоведы.",
    "tts": "Здравствуйте! Это мы, хоров+одо в+еды.",
    
    "end_session": False
  },
  "version": "1.0"
}))