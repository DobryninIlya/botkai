from .. import classes

vk = classes.vk

def group_join(request):
    object = data["object"]
    user_id = object["user_id"]
    vk.method("messages.send",
            {"peer_id": user_id, "message": "Очень жаль, что ты покинул меня. Возвращайся!", "random_id": random.randint(1, 2147483647)})
    return "ok"