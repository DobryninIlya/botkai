from .. import classes as command_class
import random
import datetime
from .. import keyboards
from ..classes import vk as vk
from ..classes import MessageSettings
from ..classes import UserParams

def info():
    today = datetime.date.today()
    chetn = UserParams.getChetn()
    if int(datetime.date(today.year, today.month, today.day).isocalendar()[1] + chetn) % 2 == 0:
        res = "Чётная"
    else:
        res = "Нечётная"
    vk.method("messages.send",
            {"peer_id": MessageSettings.getPeer_id(), "message": res , "keyboard": keyboards.getMainKeyboard(UserParams.role), "random_id": random.randint(1, 2147483647)})
    return "ok"

command = command_class.Command()

command.keys = ['четность', 'чётность', 'четность недели']
command.desciption = 'Покажу какая неделя - четная или нет'
command.process = info
command.payload = "chetnost"
command.role = [1,2,3,6]