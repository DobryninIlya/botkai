import asyncio
import datetime
import os
import traceback
import signal

from base import Bot
from botkai.classes import conn, cursor, cursorR, connection


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


def signal_handler(signal, frame):
    print('programm is down ', signal)
    cursor.close()
    cursorR.close()
    conn.close()
    connection.close()


signal.signal(signal.SIGINT, signal_handler)

if __name__ == '__main__':
    try:
        run()
    finally:
        cursor.close()
        cursorR.close()
        conn.close()
        connection.close()
        print('programm is down')
