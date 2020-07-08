import psycopg2
import vk_api
import sqlite3

class connections:
    def __init__(self):
        self.connection = psycopg2.connect(dbname='dfdn09mdk3r1gr', user='olkywigpsefwye', password='6f73707c0610067f60ed525f472fcbc34e3af291dbc21e6bec1d6d3ed89c94b9', host='ec2-54-246-121-32.eu-west-1.compute.amazonaws.com')
        self.cursor = self.connection.cursor()
        self.conn = sqlite3.connect("bot.db")
        self.cursorR = self.conn.cursor()


class vk_interface:
    def __init__(self):
        self.token = "ef9001337c74ad42b2cab874c87a2fd4bc3723bcec00355cff15130e3fb7e1643df17d9a1e4d717762780"
        self.vk = vk_api.VkApi(token=self.token)


class User:

    def __init__(self):
       self.__id = 0
       self.groupId = 0
       self.adminLevel = 0
       self.Status = 0
       self.RealGroup = 1000
       self.balance = 0
       self.name = ''
       self.dateChange = ''
       self.role = 0
       self.login = ""
    def getGroup(self):
        return self.groupId
    def getAdminLevel(self):
        return self.adminLevel
    def update(self, id):
        connection = psycopg2.connect(dbname='dfdn09mdk3r1gr', user='olkywigpsefwye', password='6f73707c0610067f60ed525f472fcbc34e3af291dbc21e6bec1d6d3ed89c94b9', host='ec2-54-246-121-32.eu-west-1.compute.amazonaws.com')
        connection.autocommit=True
        
        cursor = connection.cursor()
        res=[]
        try:
            sql = "SELECT * FROM Users WHERE ID_VK = " + str(id)
            cursor.execute(sql)
            res = cursor.fetchone()
            print("RESULT", res)
        except sqlite3.OperationalError:
            connection.commit()
            sql = "SELECT * FROM Users WHERE ID_VK = " + str(id)
            cursor.execute(sql)
            res = cursor.fetchone()
        self.groupId = res[2]
        self.adminLevel = res[4]
        self.name = res[1]
        self.RealGroup = res[5]
        self.DateChange = res[6]
        self.balance = res[7]
        self.role = res[13]
        self.login = res[14]
        #connection.close()

        
        
    def getChetn(self):
        chetn = 0 ### Четность изм. 28.01.2020
        return chetn

