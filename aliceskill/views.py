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
                    if entity["type"] == "YANDEX.NUMBER" and len(group_values) <= 4:
                        group_values += str(entity["value"])
                    elif entity["type"] == "YANDEX.DATETIME":
                        day = entity["value"]["day"]

                print(group_values)
            response["response"]["text"] = command + " " + group_values + " день " + day
            return
        else:
            response["response"]["text"] = "Я не распознал твою команду. Повтори, пожалуйста, что ты хочешь получить и номер группы."