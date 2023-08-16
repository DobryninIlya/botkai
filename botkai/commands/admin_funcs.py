import random
from datetime import date

from .. import classes as command_class
from ..keyboards import notifier_change_btn
from ..classes import vk, cursor, connection

def start_of_school_year():
    today = date.today()
    if today.month >= 8:
        return date(today.year, 9, 1)
    else:
        return date(today.year - 1, 9, 1)


async def processor(MessageSettings, user):
    if MessageSettings.payload == 'drop_groups_new_year' or MessageSettings.text == "drop_groups_new_year":
        print("ОЧИСТКА НОМЕРОВ ГРУПП СТАРОГО УЧЕБНОГО ГОДА")
        sql = "UPDATE public.users SET groupp = 100 WHERE groupp>100 AND \"dateChange\" < '{}'".format(start_of_school_year())
        res = cursor.execute(sql)
        connection.commit()
        await vk.messages.send(peer_id=MessageSettings.getPeer_id(),
                               message="*ОЧИСТКА НОМЕРОВ ГРУПП СТАРОГО УЧЕБНОГО ГОДА ПРОИЗВЕДЕНА*",
                               random_id=random.randint(1, 2147483647))

    return


command = command_class.Command()

command.keys = ['drop_groups_new_year']
command.process = processor
command.payload = "drop_groups_new_year"
command.role = [1, 2, 3, 5, 6]