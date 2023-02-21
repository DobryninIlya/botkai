import random

from .. import classes as command_class
from ..classes import vk
from ..keyboards import activities_hub

try:
    with open("/home/u_botkai/botraspisanie/botkai/botkai/commands/activities/media_debati.json", mode="rt",
              encoding="utf-8") as file:
        carousel = file.read()
except:
    with open("botkai/commands/activities/media_debati.json", mode="rt", encoding="utf-8") as file:
        carousel = file.read()


async def info(MessageSettings, user):
    await vk.messages.send(peer_id=MessageSettings.getPeer_id(),
                           message="Клуб дебатов",
                           random_id=random.randint(1, 2147483647),
                           template=carousel)


info_command = command_class.Command()

info_command.keys = ['клуб дебатов']
info_command.desciption = ''
info_command.payload = "ACT_media_debati"
info_command.process = info
