import asyncio
import datetime
import os
import traceback

from base import Bot



def run():
    loop = asyncio.get_event_loop()

    bot = Bot(os.getenv("VK_TOKEN"), 2)
    try:
        print('bot has been started')
        loop.create_task(bot.start())
        loop.run_forever()
    except KeyboardInterrupt:
        print("\nstopping", datetime.datetime.now())
        loop.run_until_complete(bot.stop())
        print('bot has been stopped', datetime.datetime.now())
    except:
        print('Ошибка:\n', traceback.format_exc())


if __name__ == '__main__':
    run()