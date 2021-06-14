from .. import classes
import random

vk = classes.vk


def group_join(request):
    data = request.body
    object = data["object"]
    user_id = object["user_id"]
    vk.method("messages.send",
              {"peer_id": user_id, "message": "Спасибо за подписку!", "random_id": random.randint(1, 2147483647)})
    return "ok"
