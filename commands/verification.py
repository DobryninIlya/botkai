import random

from .. import classes as command_class
from ..classes import vk, conn, cursorR
from ..keyboards import exit, verification


async def info(MessageSettings, user):
    try:
        cursorR.execute("INSERT INTO Status VALUES ({}, 100);".format(MessageSettings.getId()))
        conn.commit()
    except:
        await vk.messages.send(peer_id=MessageSettings.getPeer_id(),
                               message="Произошла ошибка. Повторите запрос или попробуйте позже.",
                               random_id=random.randint(1, 2147483647),
                               keyboard=verification)
        cursorR.execute("DELETE FROM Status WHERE id_vk={}".format(MessageSettings.getId()))
        conn.commit()
        return

    await vk.messages.send(peer_id=MessageSettings.getPeer_id(),
                           message="Введите логин от личного кабинета",
                           random_id=random.randint(1, 2147483647),
                           keyboard=exit)

info_command = command_class.Command()

info_command.keys = []
info_command.desciption = ''
info_command.payload = "verification"
info_command.process = info
