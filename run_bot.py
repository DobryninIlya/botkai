import asyncio
import datetime
import os
import traceback
import signal
import sys

from base import Bot
from botkai.classes import conn, cursor, cursorR, connection


def run():
    loop = asyncio.get_event_loop()

    bot = Bot(os.getenv('VK_TOKEN'), 7)
    try:
        sys.stdout.write('bot has been started\n')
        loop.create_task(bot.start())
        loop.run_forever()
        sys.stdout.flush()
    except KeyboardInterrupt:
        sys.stdout.write("\nstopping\n", str(datetime.datetime.now()))
        loop.run_until_complete(bot.stop())
        sys.stdout.write('bot has been stopped\n', str(datetime.datetime.now()))
        sys.stdout.flush()
    except:
        sys.stdout.write('\nОшибка:\n', str(traceback.format_exc()))
        sys.stdout.flush()


def signal_handler(signal, frame):
    sys.stdout.write('\nprogramm is down \n', str(signal))
    sys.stdout.flush()
    cursor.close()
    cursorR.close()
    conn.close()
    connection.close()


signal.signal(signal.SIGINT, signal_handler)

if __name__ == '__main__':
    try:
        sys.stdout.write('programm is running\n')
        sys.stdout.flush()
        run()
    except:
        print('\nОшибка (глобальная):\n', str(traceback.format_exc()), flush=True)
    finally:
        cursor.close()
        cursorR.close()
        conn.close()
        connection.close()
        print('\nprogramm is crashed\n', flush=True)
