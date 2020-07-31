import psycopg2
import vk_api
import sqlite3
import json
import traceback

class connections:
    def __init__(self):
        self.connection = psycopg2.connect(dbname='dfdn09mdk3r1gr', user='olkywigpsefwye', password='6f73707c0610067f60ed525f472fcbc34e3af291dbc21e6bec1d6d3ed89c94b9', host='ec2-54-246-121-32.eu-west-1.compute.amazonaws.com')
        self.connection.autocommit=True
        self.cursor = self.connection.cursor()
        self.conn = sqlite3.connect("bot.db")
        self.cursorR = self.conn.cursor()

connect = connections()
cursor = connect.cursor
cursorR = connect.cursorR
connection = connect.connection
conn = connect.conn

class vk_interface:
    def __init__(self):
        self.token = "ef9001337c74ad42b2cab874c87a2fd4bc3723bcec00355cff15130e3fb7e1643df17d9a1e4d717762780"
        self.vk = vk_api.VkApi(token=self.token)

vk = vk_interface().vk

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
        res=[]
        try:
            sql = "SELECT * FROM Users WHERE ID_VK = " + str(id)
            cursor.execute(sql)
            res = cursor.fetchone()
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

        
        
    def getChetn(self):
        chetn = 0 ### Четность изм. 28.01.2020
        return chetn

UserParams = User()

command_list = []
command_list_beseda = []
class Command:
    def __init__(self):
       self.__keys = []
       self.description = ''
       self.payload = ""
       self.admlevel = 0
       self.role = []
       command_list.append(self)
       self.role.append(1)
       self.role.append(3)
    def keys(self):
        return self.__keys

    def keys(self, array):
        for k in array:
            self.__keys.append(k.lower())
    def role(self, array):
        self.__role = []
        for k in array:
            self.__role.append(k)
    def Beseda(self, flag):
        if flag:
            command_list_beseda.append(self)
            command_list.remove(self)
    def process(self):
        pass



class Message:
    def __init__(self):
       self.id = 0
       self.text = ""
       self.peer_id = 0
       self.keyboard = False
       self.att = []
       self.payload = []
       self.button = ""
       self.messageId = 0
       self.statUser = 0
       self.allCommands = 0

       self.event_id = ""
       self.buttons = []
       self.conversation_message_id = 0
        
    def getId(self):
        return self.id
    def getText(self):
        return self.text
    def getPeer_id(self):
        return self.peer_id
    def getKeyboard(self):
        return self.keyboard

    def GetAttachments(self):
        print(self.att)
        attachment = ""
        for elem in self.att:
            if elem["type"] == "photo":
                photo = elem["photo"]
                attachment += "photo" + str(photo["owner_id"]) + "_" + str(photo["id"]) + ","
            elif elem["type"] == "video":
                video = elem["video"]
                attachment += "video" + str(video["owner_id"]) + "_" + str(video["id"]) + ","
            elif elem["type"] == "audio":
                audio = elem["audio"]
                attachment += "audio" + str(audio["owner_id"]) + "_" + str(audio["id"]) + ","
            elif elem["type"] == "doc":
                doc = elem["doc"]
                attachment += "doc" + str(doc["owner_id"]) + "_" + str(doc["id"]) + ","
                #attachment += str(doc["url"]) + ","

            try:
                attachmentRes = attachment[:-1]
                attachmentRes += "_" + elem[elem["type"]]["access_key"] + ","
                attachment = attachmentRes
            except Exception as E:
                pass
        
        return attachment[:-1]
    def GetTaskCount(self, date, group):
        connection = psycopg2.connect(dbname='dfdn09mdk3r1gr', user='olkywigpsefwye', password='6f73707c0610067f60ed525f472fcbc34e3af291dbc21e6bec1d6d3ed89c94b9', host='ec2-54-246-121-32.eu-west-1.compute.amazonaws.com')
        cursor = connection.cursor()
        sql = "SELECT COUNT(*) FROM Task WHERE GroupID = " + str(group) + " AND Datee = '" + date + "'"
        cursor.execute(sql)
        res = cursor.fetchone()
        connection.close()
        return res[0]
    def GetAdv(self, date, group):
        connection = psycopg2.connect(dbname='dfdn09mdk3r1gr', user='olkywigpsefwye', password='6f73707c0610067f60ed525f472fcbc34e3af291dbc21e6bec1d6d3ed89c94b9', host='ec2-54-246-121-32.eu-west-1.compute.amazonaws.com')
        cursor = connection.cursor()
        sql = 'SELECT textfield FROM "Adv" WHERE groupid = ' + str(group) + " AND date = '" + date + "' ORDER BY id DESC"
        cursor.execute(sql)
        res = cursor.fetchone()
        connection.close()
        try:
            return str(res[0])
        except Exception as E:
            pass
        return ""
    def Clear(self):
        self.id = 0
        self.text = ""
        self.peer_id = 0
        self.keyboard = False
        self.att = []
        self.payload = []
        self.button = ""

        return
    def update(self, message_params):
        if message_params["type"] == "message_event":
            self.event_id = message_params["object"]["event_id"]
            self.id = message_params["object"]["user_id"]
            self.peer_id = message_params["object"]["peer_id"]
            self.buttons = []
            self.conversation_message_id = int(message_params["object"]["conversation_message_id"])
            try:
                self.payload = message_params["object"]["payload"]
            except KeyError:
                self.payload = None
            except:
                print('Ошибка:\n', traceback.format_exc())  
            return
        self.id = int(message_params["object"]["message"]["from_id"])
        self.text = message_params["object"]["message"]["text"]
        self.peer_id = int(message_params["object"]["message"]["peer_id"])
        self.keyboard = False
        try:
            self.payload = json.loads(message_params["object"]["message"]["payload"])
        except KeyError:
            self.payload = None
        self.messageId = message_params["object"]["message"]["id"]
        if message_params["object"]["message"]["attachments"]:
            res = vk.method("messages.getById",{"message_ids": self.messageId})
            res = res["items"][0]["attachments"]
            self.att = res
        else:
            self.att = ""


        self.statUser = 0
        self.allCommands = 0
        if message_params["type"] == "message_new":
            self.buttons = message_params["object"]["client_info"]["button_actions"]
            self.conversation_message_id = 0

            
    
MessageSettings = Message()