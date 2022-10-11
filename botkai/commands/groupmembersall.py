import random

import aiohttp
import requests
from bs4 import BeautifulSoup

from .. import classes as command_class
from ..classes import vk, MessageSettings, UserParams


async def info():
    msg = "Запрос отправлен на обработку"
    msg_id = await vk.messages.send(peer_id=MessageSettings.getPeer_id(),
                           message=msg,
                           random_id=random.randint(1, 2147483647))
    i = 1
    async with aiohttp.ClientSession() as session:
        async with await session.post(("https://kai.ru/infoClick/-/info/group?id={id}").format(id=UserParams.groupId)) as response:
            response = await response.text()
    soup = BeautifulSoup(response, 'lxml')

    # print(soup.find("ul", attrs={ "id" : "mylist"}))
    list_students = soup.find(id="p_p_id_infoClick_WAR_infoClick10_")
    result = ""
    if not response:
        result = "Данные не найдены на сайте КАИ."
        await vk.messages.edit(peer_id=MessageSettings.getPeer_id(),
                               message=result,
                               message_id=msg_id)
    for tag in list_students.find_all("td"):
        if len(tag.text) > 6:
            result += str(i) + ". " + tag.text.strip().replace("\n", "").replace(
                "                                                                Староста", " (🙋 Староста)") + "\n"
            i += 1
    await vk.messages.edit(peer_id=MessageSettings.getPeer_id(),
                           message=result,
                           message_id=msg_id)
    return "ok"


command = command_class.Command()

command.keys = ['список группы', 'мои одногруппники']
command.desciption = 'отображение полного списка группы'
command.process = info
command.payload = "groupmembersall"
