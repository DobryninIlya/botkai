import random
import traceback


class Spam_Handler:
    def __init__(self, message, vk):
        self.conversation_message_id = message.conversation_message_id
        self.peer_id = message.peer_id
        self.text = message.text
        self.from_id = message.from_id
        self.vk = vk
        self.base = ['солдат', 'слили', 'в канале', 'переходи', 'Telegram', 'кадры', 'зверский', 'мобилизация', 'предложение', 'руб',
                     'цензуры', 'сеть', 'обман', 'правительство', 'nemchinowa', 'tapy.me', 'https://', 'www.', 'vk.cc', 'clck',
                                        'мобилизац', 'в канал', 'сет', 'зверск', 'ссылк']

    async def handle_text_message(self):
        message = self.text.lower().split()
        score = 0
        for word in message:
            if word in self.base:
                score += 1
                continue
            for word_ in self.base:
                if word_ in word:
                    score += 1
                    continue
        flag = True if 't.me/+' in self.text.lower() else False
        for word in self.text.lower():
            if word in ['t.me/+', 'clck.ru', 'vk.cc', 'goo.gl', 'to.click', 'bit.do', 'ow.ly']
        if flag and score >= 1:
            try:
                await self.vk.messages.delete(delete_for_all=1,
                                              peer_id=str(self.peer_id),
                                              cmids=str(self.conversation_message_id)
                                              )
                await self.vk.messages.send(peer_id=self.peer_id,
                                            message="[chat-guardian]: Удален спам.",
                                            random_id=random.randint(1, 2147483647))
            except:
                await self.vk.messages.send(peer_id=self.peer_id,
                                            message="Это сообщение помечено как СПАМ, но пока я не могу его удалить :(",
                                            random_id=random.randint(1, 2147483647))
        else:
            return False
