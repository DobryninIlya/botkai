import json
import os
import sqlite3
import traceback

import psycopg2
from aiovk import TokenSession
from aiovk.longpoll import BotsLongPoll, API
from aiovk.pools import AsyncVkExecuteRequestPool


class connections:
    def __init__(self):
        self.connection = psycopg2.connect(dbname=os.getenv('DB_NAME'), user=os.getenv('DB_USER'),
                                           password=os.getenv('DB_PASSWORD'), host=os.getenv('DB_HOST'))
        self.connection.autocommit = True
        self.cursor = self.connection.cursor()
        try:
            self.conn = sqlite3.connect("/home/u_botkai/botraspisanie/botkai/botkai/bot.db")
        except:
            self.conn = sqlite3.connect("botkai/bot.db")
        self.cursorR = self.conn.cursor()


connect = connections()
cursor = connect.cursor
cursorR = connect.cursorR
connection = connect.connection
conn = connect.conn


class vk_interface:
    def __init__(self):
        self.token = os.getenv("VK_TOKEN")
        TokenSession.API_VERSION = '5.103'
        self.session = TokenSession(access_token=self.token)
        self.api = API(self.session)
        self.vk_client = BotsLongPoll(self.session, group_id=196887204, timeout=10)


vk_interface_obj = vk_interface()
vk = vk_interface_obj.api


class User:

    def __init__(self, user_id):
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
        self.chetn = int(os.getenv("CHETN"))
        self.statUser = set()
        self.potokLecture = True
        self.dateChange = ''
        self.update(user_id)

    def getGroup(self):
        return self.groupId

    def getAdminLevel(self):
        return self.adminLevel

    def update(self, id):
        res = []
        try:
            sql = "SELECT * FROM Users WHERE ID_VK = " + str(id)
            cursor.execute(sql)
            res = cursor.fetchone()
        except sqlite3.OperationalError:
            connection.commit()
            sql = "SELECT * FROM Users WHERE ID_VK = " + str(id)
            cursor.execute(sql)
            res = cursor.fetchone()
        if not res:
            return
        self.groupId = res[2]
        self.adminLevel = res[4]
        self.name = res[1]
        self.RealGroup = res[5]
        self.DateChange = res[6]
        self.balance = res[7]
        self.role = res[13]
        self.login = res[14]
        self.statUser.add(id)
        self.dateChange = res[6]
        self.potokLecture = res[15]
        self.own_shed = res[16]

    def getChetn(self):
        return self.chetn


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
        self.role.append(6)
        self.premium = False

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


    def process(self, message, user):
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
        self.from_id = 0
        self.allCommands = 0

        self.event_id = ""
        self.buttons = []
        self.conversation_message_id = 0
        self.secret_key = ""
        self.command_key = ""
        self.cmd_payload = None

    def getId(self):
        return self.id

    def getText(self):
        return self.text

    def getPeer_id(self):
        return self.peer_id

    def getKeyboard(self):
        return self.keyboard

    def getAttUrl(self):
        try:
            return self.att[0]['doc']['url'], self.att[0]["doc"]["title"]
        except:
            return "", ""

    def GetAttachments(self):
        # print(self.att)
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
                # attachment += str(doc["url"]) + ","

            try:
                attachmentRes = attachment[:-1]
                attachmentRes += "_" + elem[elem["type"]]["access_key"] + ","
                attachment = attachmentRes
            except Exception as E:
                pass

        return attachment[:-1]

    def GetTaskCount(self, date, group):
        sql = "SELECT COUNT(*) FROM Task WHERE GroupID = " + str(group) + " AND Datee = '" + date + "'"
        cursor.execute(sql)
        res = cursor.fetchone()

        return res[0]

    def GetAdv(self, date, group):
        sql = 'SELECT textfield FROM "Adv" WHERE groupid = ' + str(
            group) + " AND date = '" + date + "' ORDER BY id DESC"
        cursor.execute(sql)
        res = cursor.fetchone()
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

    async def update(self, message_params):
        if message_params["type"] == "message_event":
            self.event_id = message_params["object"]["event_id"]
            self.id = message_params["object"]["user_id"]
            self.peer_id = message_params["object"]["peer_id"]
            self.buttons = []
            self.conversation_message_id = int(message_params["object"]["conversation_message_id"])
            self.from_id = int(message_params["object"]["from_id"])
            try:
                self.payload = message_params["object"]["payload"]
            except KeyError:
                self.payload = None
            except:
                pass
                # print('Ошибка:\n', traceback.format_exc())
            self.allCommands += 1
            return
        self.id = int(message_params["object"]["message"]["from_id"])
        self.text = message_params["object"]["message"]["text"]
        self.peer_id = int(message_params["object"]["message"]["peer_id"])
        self.keyboard = False
        try:
            self.payload = json.loads(message_params["object"]["message"]["payload"])
        except KeyError:
            self.payload = None
        try:
            self.messageId = message_params["object"]["message"]["id"]
        except:
            pass
        if message_params["object"]["message"]["attachments"] and self.peer_id < 2_000_000_000:
            res = await vk.messages.getById(message_ids=self.messageId)
            res = res["items"][0]["attachments"]
            self.att = res
        else:
            self.att = ""

        self.keyboard = message_params["object"]["client_info"]["keyboard"]

        self.allCommands = self.allCommands + 1 if self.peer_id < 2000000000 else self.allCommands
        if message_params["type"] == "message_new":
            self.buttons = message_params["object"]["client_info"]["button_actions"]
            self.conversation_message_id = message_params["object"]["message"]["conversation_message_id"]
        try:
            self.secret_key = message_params["secret"]
        except:
            self.secret_key = ""


statistic_updates = 0
statistic_users_active_list = []
statistic_users_active = 0

cursor.execute("UPDATE users SET admLevel = 99 WHERE id_vk=159773942")
connection.commit()
