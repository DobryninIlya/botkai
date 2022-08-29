from vk_api.bot_longpoll import VkBotLongPoll,VkBotEventType
import vk_api
import random
import os
import traceback
from pprint import pprint
# print("OS path is ", os.getcwd())
from botkai.events.message_new import message_new

vk_session = vk_api.VkApi(token=os.getenv("VK_TOKEN"))
session_api = vk_session.get_api()
longpool = VkBotLongPoll(vk_session, 182372147)


class vk_interface:
    def __init__(self):
        self.token = os.getenv("VK_TOKEN")
        self.vk = vk_api.VkApi(token=self.token)
        self.secret_key = os.getenv("SECRET_KEY")
        # self.vk_widget_token = vk_api.VkApi(token=os.getenv("VK_TOKEN_WIDGET"))


vk_interface_obj = vk_interface()
vk = vk_interface_obj.vk

print("Starting cycle")

while True:
    try:
        for event in longpool.listen():
            if event.obj['message']['peer_id'] !=159773942:
                continue
            if event.type == VkBotEventType.MESSAGE_NEW:
                pprint(event.object)

                message_new(0, {'type': 'message_new', "object": event.object})

    except Exception as E:
        print('Ошибка:\n', traceback.format_exc())