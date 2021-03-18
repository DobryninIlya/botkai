from .. import classes as command_class
from ..keyboards import keyboardicalendarGuide
from ..classes import vk, MessageSettings, UserParams
import random
import requests


def GetDocShedule(group, id):
    message = "https://dobrynin.engineer/download/shedule/?groupid={}".format(UserParams.groupId)
    with open('{}.txt'.format(group), 'w') as f:
        f.write(str(message))
    a = vk.method("docs.getMessagesUploadServer", { "type" : "doc", "peer_id": id })
    b = requests.post(a["upload_url"], files= { "file" : open(str(group)+".txt", "rb")}).json()
    c = vk.method("docs.save", {"file" : b["file"]})
    d = "doc"+str(c["doc"]["owner_id"])+"_"+str(c["doc"]["id"])
    return d

def info():

    message = """URL ссылка на календарь позволяет добавить ваше расписание в онлайн календари, например в Outlook. 
    Такое расписание не нужно скачивать, календарь автоматически скачает его по этой ссылке.
    Просто скопируйте эту ссылку и вставьте в ваш календарь.
    """
    vk.method("messages.send",
                    {"peer_id": MessageSettings.getPeer_id(), "message": message, "keyboard" : keyboardicalendarGuide,
                        "random_id": random.randint(1, 2147483647)})
    # message = "https://dobrynin.engineer/download/shedule/?groupid={}".format(UserParams.groupId)
    message = "Откройте файл и скопируйте ссылку."
    vk.method("messages.send",
              {"peer_id": MessageSettings.getPeer_id(), "message": message,
               'attachment' : GetDocShedule(UserParams.groupId, MessageSettings.getId()),
               "random_id": random.randint(1, 2147483647)})

info_command = command_class.Command()

info_command.keys = ['url ссылка на календарь']
info_command.desciption = 'ссылка на календарь в Интернете для добавления в онлайн календари'
info_command.payload = "url_shed_ics"
info_command.process = info
