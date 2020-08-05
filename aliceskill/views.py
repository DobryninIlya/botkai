from __future__ import unicode_literals
from django.http import HttpResponse
# Импортируем модули для работы с JSON и логами.
import json
import logging
from django.views.decorators.csrf import csrf_exempt
from pprint import pprint

sessionStorage = {}
commands = ['расписание']

logging.basicConfig(level=logging.DEBUG)

@csrf_exempt
def main(request):
# Функция получает тело запроса и возвращает ответ.
    body = json.loads(request.body)
    pprint(body)

    response = {
        "version": body['version'],
        "session": body['session'],
        "response": {
            "end_session": False
        }
    }

    handle_dialog(body,request, response)

    return HttpResponse( json.dumps( response))


def handle_dialog(body, request, response):
    request = body["request"]
    tokens = request["nlu"]["tokens"]
    entities = request["nlu"]["entities"]
    group_values = ""
    for command in commands:
        if command.lower() in tokens:
            print("Command ", command.lower())
            command = command.lower()
            if command == 'расписание':
                for entity in entities:
                    if entity["type"] == "YANDEX.NUMBER":
                        group_values += str(entity["value"])
                print(group_values)
            response["response"]["text"] = command + " " + group_values
            return