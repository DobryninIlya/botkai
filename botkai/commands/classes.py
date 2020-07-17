import psycopg2
from message_class import MessageSettings
import sqlite3

def StatusR(id): ### Текущий статус в таблице Status (RAM)
    conn = sqlite3.connect("bot.db")
    cursorR = conn.cursor()
    sql = "SELECT Status FROM Status WHERE ID_VK=" + str(id)
    cursorR.execute(sql)
    res=cursorR.fetchall()
    #print(int((str(res))[2:-3]))
    try:
        if int(res[0][0]) > 0:
            conn.close()
            return int(res[0][0])
        else:
            conn.close()
            return 0
    except IndexError:
        return 0
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
    def update(self):
        connection = psycopg2.connect(dbname='dfdn09mdk3r1gr', user='olkywigpsefwye', password='6f73707c0610067f60ed525f472fcbc34e3af291dbc21e6bec1d6d3ed89c94b9', host='ec2-54-246-121-32.eu-west-1.compute.amazonaws.com')
        cursor = connection.cursor()
        res=[]
        try:
            sql = "SELECT * FROM Users WHERE ID_VK = " + str(MessageSettings.getId())
            cursor.execute(sql)
            res = cursor.fetchone()
        except sqlite3.OperationalError:
            connection.commit()
            sql = "SELECT * FROM Users WHERE ID_VK = " + str(MessageSettings.getId())
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
        connection.close()

        self.Status = StatusR(MessageSettings.getId())
        
    def getChetn(self):
        chetn = 0 ### Четность изм. 28.01.2020
        return chetn


UserParams = User()