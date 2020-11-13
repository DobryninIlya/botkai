from locust import HttpUser, TaskSet, task, user


def get_pattern(payload):
    return """{
        "type": "message_new",
        "object": {
            "message": {
                "date": 1605284570,
                "from_id": 159773942,
                "id": 600265,
                "out": 0,
                "peer_id": 159773942,
                "text": "Понедельник",
                "conversation_message_id": 92,
                "fwd_messages": [],
                "important": False,
                "random_id": 0,
                "attachments": [],
                "payload": {\"button\":\"tomorrow\"},
                "is_hidden": False
            },
            "client_info": {
                "button_actions": [
                    "text",
                    "vkpay",
                    "open_app",
                    "location",
                    "open_link",
                    "open_photo",
                    "callback"
                ],
                "keyboard": True,
                "inline_keyboard": True,
                "carousel": True,
                "lang_id": 0
            }
        },
        "group_id": 182372147,
        "event_id": "a44f528a5b29ef11b5cda565291cabf2736c3b17",
        "secret" : "dhJHnr9Kv4jsI8rjiANmsdO73ZoWf9ol1XTphK9DJbVk6dufE"
    }"""

class UserBehavior(TaskSet):
    def on_start(self):
        self.client.post("/botkai/", get_pattern("{\"button\":\"tomorrow\"}"))

    def on_stop(self):
        self.client.post("/botkai/", get_pattern("{\"button\":\"tomorrow\"}"))

    @task(2)
    def index(self):
        self.client.get("/botkai/", get_pattern("{\"button\":\"tomorrow\"}"))

    @task(1)
    def profile(self):
        self.client.get("/botkai/",get_pattern("{\"button\":\"tomorrow\"}"))


class User(HttpUser):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000
    def on_start(self):
        self.client.post("/botkai/", get_pattern("{\"button\":\"tomorrow\"}"))

    def on_stop(self):
        self.client.post("/botkai/", get_pattern("{\"button\":\"tomorrow\"}"))

    @task(2)
    def index(self):
        self.client.post("/botkai/", get_pattern("{\"button\":\"tomorrow\"}"))

    @task(1)
    def profile(self):
        self.client.post("/botkai/",get_pattern("{\"button\":\"tomorrow\"}"))
