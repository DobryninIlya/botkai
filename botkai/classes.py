import psycopg2

class connections:
    def __init__(self):
        self.connection = psycopg2.connect(dbname='dfdn09mdk3r1gr', user='olkywigpsefwye', password='6f73707c0610067f60ed525f472fcbc34e3af291dbc21e6bec1d6d3ed89c94b9', host='ec2-54-246-121-32.eu-west-1.compute.amazonaws.com')
        self.cursor = self.connection.cursor()
        conn = sqlite3.connect("bot.db")
        cursorR = conn.cursor()


class vk_interface:
    def __init__(self):
        token = "464ef8b3e89a0963631f63fc198ce51fa7dd368ade4e99fa8a6d45f6f8f628b6086bf35f0e720ad9b6d4c"
        vk = vk_api.VkApi(token=token)
