from .. import classes as command_class
from ..classes import vk, MessageSettings, UserParams
import random
import json
# from ..keyboards import 


buildings = {
    1 : {
        'lat' : 55.796707,
        'long': 49.11506,
        'chislit' : 'Первый'
    },
    2 : {
        'lat' : 55.82267,
        'long': 49.13615,
        'chislit' : 'Второй'
    },
    3 : {
        'lat' : 55.79238,
        'long': 49.13748,
        'chislit' : 'Третий'
    },
    4 : {
        'lat' : 55.79354,
        'long': 49.13762,
        'chislit' : 'Четвертый'
    },
    5 : {
        'lat' : 55.7964,
        'long': 49.12475,
        'chislit' : 'Пятый'
    },
    6 : {
        'lat' : 55.854202,
        'long': 49.11506,
        'chislit' : 'Шестой'
    },
    7 : {
        'lat' : 55.7971,
        'long': 49.135,
        'chislit' : 'Седьмой'
    },
    8 : {
        'lat' : 55.82086,
        'long': 49.136154,
        'chislit' : 'Восьмой'
    }

}


def info():


    num = MessageSettings.payload['number']
    
    vk.method("messages.send",
                {"peer_id": MessageSettings.getPeer_id(), "message": "{} дом".format(buildings[int(num)]['chislit']), 'lat' : buildings[int(num)]['lat'], 'long' : buildings[int(num)]['long'],
                    "random_id": random.randint(1, 2147483647)})

info_command = command_class.Command()

info_command.keys = ['']
info_command.desciption = 'здания'
info_command.payload = "buildings_num"
info_command.process = info
