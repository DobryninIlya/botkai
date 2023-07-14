from .. import classes as command_class

from ..keyboards import notifier_change_btn
from ..classes import vk, cursor, connection
import random

msg = "Ваш статус оповещения об изменениях в расписании: *{}*. \nХотите изменить?"
msg_changed = "Статус оповещения изменен на: *{}*"

async def processor(MessageSettings: command_class.Message, user):
    cursor.execute("SELECT schedule_change FROM notify_clients WHERE destination_id = {dId} AND source = '{source}'".format(
        dId=MessageSettings.getPeer_id(),
        source="vk"
    ))
    result_query = cursor.fetchone()
    if result_query == None:
        cursor.execute("INSERT INTO notify_clients (id, destination_id, schedule_change, source) VALUES ("
                       "(SELECT COUNT(*) FROM notify_clients), {id}, true, 'vk');".format(id=MessageSettings.getPeer_id()))
        result_query = [True]

    flag: bool = result_query[0]
    if MessageSettings.payload:
        if MessageSettings.payload['button'] == "notifier_change":
            flag = not flag
            cursor.execute(
                "UPDATE notify_clients SET schedule_change = {flag} WHERE destination_id = {dId} AND source = '{source}'".format(
                    flag=flag,
                    dId=MessageSettings.getPeer_id(),
                    source="vk"
                ))
            connection.commit()
            message_send = msg_changed.format("Неактивно" if not flag else "Активно")
            await vk.messages.send(peer_id=MessageSettings.getPeer_id(),
                                   message=message_send,
                                   keyboard=notifier_change_btn,
                                   random_id=random.randint(1, 2147483647))
            return
    message_send = msg.format("Активно" if flag else "Неактивно")
    await vk.messages.send(peer_id=MessageSettings.getPeer_id(),
                           message=message_send,
                           keyboard=notifier_change_btn,
                           random_id=random.randint(1, 2147483647))
    return


command = command_class.Command()

command.keys = ["изменить оповещения", "оповещения изменить", "изменения в расписании"]
command.process = processor
command.payload = "notifier_change"
