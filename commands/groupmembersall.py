import random

import requests
from bs4 import BeautifulSoup

from .. import classes as command_class
from ..classes import vk, MessageSettings, UserParams


def info():
    msg = "Запрос отправлен на обработку"
    msg_id = vk.method("messages.send",
                    {"peer_id": MessageSettings.id, "message": msg, "random_id": random.randint(1, 2147483647)})
    i = 1
    response = requests.post(("https://kai.ru/infoClick/-/info/group?id={id}").format(id = UserParams.groupId))
    soup = BeautifulSoup(response.text, 'lxml')

    # print(soup.find("ul", attrs={ "id" : "mylist"}))
    list_students = soup.find(id="p_p_id_infoClick_WAR_infoClick10_")
    result = ""
    for tag in list_students.find_all("td"):
        if len(tag.text) > 6:

            result += str(i) + ". " + tag.text.strip().replace("\n", "").replace(
                "                                                                Староста", " (🙋 Староста)") + "\n"
            i+=1
    vk.method("messages.edit", {"peer_id": MessageSettings.id, "message_id": msg_id ,"message": result})


    return "ok"




command = command_class.Command()




command.keys = ['список группы', 'мои одногруппники']
command.desciption = 'отображение полного списка группы'
command.process = info
command.payload = "groupmembersall"