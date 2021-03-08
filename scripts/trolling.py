import vk_api
import os
import random
from pprint import pprint

class vk_interface:
    def __init__(self):
        self.token = os.getenv("VK_TOKEN")
        self.vk = vk_api.VkApi(token=self.token)
        self.secret_key = os.getenv("SECRET_KEY")
vk_interface_obj = vk_interface()
vk = vk_interface_obj.vk

while(True):
    messages = vk.method("messages.getConversations", {"offset": 0, "count": 1})
    if messages["count"] >= 1:
        id = messages["items"][0]["last_message"]["from_id"]
        body = messages["items"][0]["last_message"]["text"]

        if id == 159773942:
            pprint(messages)
            vk.method("messages.send", {"peer_id": messages["items"][0]["conversation"]["peer"]["id"], "message": "Да, кикнуть", "random_id": random.randint(1, 2147483647)})