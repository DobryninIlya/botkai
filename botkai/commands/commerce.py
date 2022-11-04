import random

from .. import classes as command_class
from ..classes import vk


async def info(MessageSettings, user):
    message= """Помогу в написании программной реализации проекта
    Напишу программу с GUI интерфейсом или чат-бота на интересную тему. Пишите с вопросами в личные сообщения. 
    Все конфиденциально.
    Мой телеграм - https://dobryninilya.t.me"""
    await vk.messages.send(peer_id=MessageSettings.getPeer_id(),
                           message=message,
                           random_id=random.randint(1, 2147483647))


info_command = command_class.Command()

info_command.keys = []
info_command.desciption = 'разработка дипломов'
info_command.payload = "commerce"
info_command.process = info

