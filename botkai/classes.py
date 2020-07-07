import psycopg2

class connections:
    def __init__(self):
        self.connection = psycopg2.connect(dbname='dfdn09mdk3r1gr', user='olkywigpsefwye', password='6f73707c0610067f60ed525f472fcbc34e3af291dbc21e6bec1d6d3ed89c94b9', host='ec2-54-246-121-32.eu-west-1.compute.amazonaws.com')
        self.cursor = self.connection.cursor()
        conn = sqlite3.connect("bot.db")
        cursorR = conn.cursor()


class vk_interface:
    def __init__(self):
        token = "ef9001337c74ad42b2cab874c87a2fd4bc3723bcec00355cff15130e3fb7e1643df17d9a1e4d717762780"
        vk = vk_api.VkApi(token=token)

