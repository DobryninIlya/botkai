import random
import traceback
from .classes import cursor, connection


class Spam_Handler:
    def __init__(self, message, vk):
        self.conversation_message_id = message.conversation_message_id
        self.peer_id = message.peer_id
        self.text = message.text
        self.from_id = message.id
        self.is_picture_att = 'photo' in message.GetAttachments()
        self.vk = vk
        self.base = ['солдат', 'слили', 'в канале', 'переходи', 'telegram', 'кадры', 'зверский', 'мобилизация', 'предложение', 'руб',
                     'цензуры', 'сеть', 'обман', 'правительство', 'nemchinowa', 'tapy.me', 'https://', 'www.',
                                        'мобилизац', 'в канал', 'сет', 'зверск', 'ссылк', 'телеграм', 'nemchinova', '100%', 'болельщи',
                     'пушк', 'карт', 'лото', 'правительство', 'путин', 'pus', 'лотер', 'куплю', 'купить',
                     'приз', 'букм']
        self.domains = ['t.me/+', 'clck.ru', 'vk.cc', 'goo.gl', 'to.click', 'bit.do', 'ow.ly', 'socprofile.com',
                        'bit.ly', 'tinyurl.com', 'tiny.one', 'rotf.lol', 'u.to']


    async def handle_text_message(self):
        message = self.text.lower().split()
        score = 0
        flag = False
        for word in message:
            if word in self.base:
                score += 1
                continue
            for word_ in self.base:
                if word_ in word:
                    score += 1
                    continue
            for part_word in self.domains: # Проверка доменных имен
                if part_word in word:
                    flag = True
                    break
        mode = 'standart'
        silent = False
        cmd = self.text.lower()
        try:
            if cmd[0]=='!':
                if self.from_id != 159773942:
                    await self.vk.messages.send(peer_id=self.peer_id,
                                           sticker_id=20476,
                                           random_id=random.randint(1, 2147483647))
                    return
                if cmd[1:5] == 'mode':
                    mode = cmd[6:]
                    try:
                        sql = "UPDATE g_chat SET decor_mode = '{}' WHERE id={}".format(mode, self.peer_id)
                        cursor.execute(sql)
                        connection.commit()
                        await self.vk.messages.send(peer_id=self.peer_id,
                                                    message="[chat-guardian]: Установлен режим {} в чат {}".format(mode, str(self.peer_id)[5:]),
                                                    random_id=random.randint(1, 2147483647))
                    except:
                        print('Ошибка:\n', traceback.format_exc())

                elif cmd[1:7] == 'silent':
                    silent = True if cmd[8:] == 'yes' else False
                    try:
                        sql = "UPDATE g_chat SET silent_mode = {}".format(silent, self.peer_id)
                        cursor.execute(sql)
                        connection.commit()
                        await self.vk.messages.send(peer_id=self.peer_id,
                                                    message="[chat-guardian]: Установлено отображение уведомлений {} в чат {}".format('ВСЕ' if not silent else 'ТИХИЙ',
                                                                                                                   str(self.peer_id)[5:]),
                                                    random_id=random.randint(1, 2147483647))
                    except:
                        print('Ошибка:\n', traceback.format_exc())

            # print("mode {}\nsilent {}".format(mode, silent))
        except:
            return

        if flag and (score >= 1 or self.is_picture_att):
            sql = "SELECT * FROM g_chat WHERE id = {}".format(self.peer_id)
            cursor.execute(sql)
            query_result = cursor.fetchone()
            if not query_result: # не зарегистрирован
                sql_query = "INSERT INTO g_chat VALUES ({}, '{}', {})".format(self.peer_id, mode, silent)
                cursor.execute(sql_query)
                connection.commit()
            else:
                mode = query_result[1].rstrip().lower()
                silent = query_result[2]
            try:
                await self.vk.messages.delete(delete_for_all=1,
                                              peer_id=str(self.peer_id),
                                              cmids=str(self.conversation_message_id)
                                              )
                if silent:
                    return
                if mode == 'amongus':
                    await self.vk.messages.send(peer_id=self.peer_id,
                                                message="*id{} (Пользователь) оказался предателем....".format(self.from_id),
                                                random_id=random.randint(1, 2147483647))
                else:
                    await self.vk.messages.send(peer_id=self.peer_id,
                                            message="[chat-guardian]: Удален спам.",
                                            random_id=random.randint(1, 2147483647))
            except:
                await self.vk.messages.send(peer_id=self.peer_id,
                                            message="Это сообщение помечено как СПАМ, но пока я не могу его удалить :(",
                                            random_id=random.randint(1, 2147483647))
        else:
            return False
