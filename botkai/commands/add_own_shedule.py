import random

import requests

from .. import classes as command_class
from ..classes import vk, MessageSettings


def GetDocShedule(id):
    a = vk.method("docs.getMessagesUploadServer", {"type": "doc", "peer_id": id})
    b = requests.post(a["upload_url"], files={"file": open("shed_example.xlsx", "rb")}).json()
    c = vk.method("docs.save", {"file": b["file"]})
    d = "doc" + str(c["doc"]["owner_id"]) + "_" + str(c["doc"]["id"])
    return d


def info():
    id = MessageSettings.getId()

    vk.method("messages.send",
                        {"peer_id": id, "message": "Заполните бланк расписания. Инструкции по заполнению указаны в файле (колонка справа)"
                                                   "Как заполните расписание - прикрепите файл к сообщению с текстом 'загрузить расписание' и отправьте его", "attachment": GetDocShedule(id), "random_id": random.randint(1, 2147483647)})

    return "ok"



command = command_class.Command()




command.keys = ['добавить свое расписание']
command.desciption = 'добавить свое расписание'
command.process = info
command.payload = "add_own_shedule"

