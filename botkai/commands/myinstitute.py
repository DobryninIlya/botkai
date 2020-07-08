import command_class
import vk_api
import random
import keyboards
from main import vk, uptime
from message_class import MessageSettings
from user_class import UserParams
from keyboards import KeyboardProfile
import datetime
import sqlite3
import psycopg2
import traceback


def info():
    id = MessageSettings.getId()
    group = UserParams.RealGroup
    if group == 0:
        vk.method("messages.send",
                {"peer_id": id, "message": "Сначала подтверди группу в профиле", "keyboard" : KeyboardProfile(), "random_id": random.randint(1, 2147483647)})
        return "ok"

    fdigit = group // 1000
    ldigit = group % 100
    mesg = ""
    header = ""
    adress = "\nАдрес: "
    phone = "\nТелефон/факс: "
    mail =  "\nE-mail: "
    hours = "\nЧасы работы дирекции: "
    vkid = "\n@"
    comm = "\n Беседа: "
    if fdigit == 9:
        header += "ИНСТИТУТ ИНЖЕНЕРНОЙ ЭКОНОМИКИ И ПРЕДПРИНИМАТЕЛЬСТВА"
        adress += "г. Казань, ул. Четаева, 18 (2-е учебное здание КНИТУ-КАИ), к. 423, 439, 442"
        phone += "+7 (843) 231-02-36"
        mail += "ieust@kai.ru"
        hours += "с 9:00 до 17:00"
        vkid += "ieustru" + " (Дирекция)"
        comm += "https://vk.me/join/AJQ1dxGifxaEPMPygQVm9qLX"
    elif fdigit == 4:
        if ldigit < 30:
            header += "ИНСТИТУТ КОМПЬЮТЕРНЫХ ТЕХНОЛОГИЙ И ЗАЩИТЫ ИНФОРМАЦИИ"
            adress += "г. Казань, ул. Б. Красная, 55 (7-е учебное здание КНИТУ-КАИ)"
            phone += "+7 (843) 231 16 51, +7 (843) 231 00 85"
            mail += "itki@kai.ru"
            hours += "с 9:00 до 17:00"
            vkid += "dean4" + " (Дирекция)"
        elif ldigit > 30:
            header += "КОЛЛЕДЖ ИНФОРМАЦИОННЫХ ТЕХНОЛОГИЙ"
            adress += " г. Казань, ул. Большая Красная 55, каб. 116 - 116а,  1 этаж"
            phone += "+7 (843) 231-00-00, 231-00-05"
            mail += "kit@kai.ru"
            hours += "с 9:00 до 17:00"
            vkid += "kai_kit" + " (Дирекция)"
        comm += "https://vk.me/join/AJQ1dxtIZRad4MxP05/B0dz0"
    elif fdigit == 5:
        header += "ИНСТИТУТ РАДИОЭЛЕКТРОНИКИ И ТЕЛЕКОММУНИКАЦИЙ"
        adress += "г. Казань, ул. Карла Маркса, 31/7 (5-е учебное здание КНИТУ-КАИ)"
        phone += """Дневное отделение +7 (843) 231 59 12
Заочное отделение +7 (843) 231 59 13"""
        mail += "-"
        hours += "с 9:00 до 17:00"
        vkid += "kai_iret" + " (Дирекция)"
        comm += "https://vk.me/join/AJQ1d6P6hxYB8ieBeomCDGEL"
    elif fdigit == 3:
        header += "ИНСТИТУТ АВТОМАТИКИ И ЭЛЕКТРОННОГО ПРИБОРОСТРОЕНИЯ" 
        adress += "г. Казань, ул. Толстого, 15 (3-е учебное здание КНИТУ-КАИ)"
        phone += """+7 (843) 231 03 94"""
        mail += "dekanat3@mail.ru"
        hours += "с 9:00 до 17:00"
        vkid += "public42139288" + " (Дирекция)"
        comm += "https://vk.me/join/AJQ1d6qdihb54WBjpLS0foQ9"
    elif fdigit == 2:
        header += "ФИЗИКО-МАТЕМАТИЧЕСКИЙ ФАКУЛЬТЕТ" 
        adress += "г. Казань, ул. Четаева, 18 ​(2-е учебное здание КНИТУ-КАИ)"
        phone += """декан: +7 (843) 231 02 04, 231 16 44;
диспетчер: +7 (843) 231 02 08;
факс: +7 (843) 231 02 08."""
        mail += "fmf@kai.ru"
        hours += "с 9:00 до 17:00"
        vkid += "kaifmf" + " (Дирекция)"
        comm += "https://vk.me/join/AJQ1d_DGbRaDtOaV3kNl2GA7"
    elif fdigit == 1:
        header += "ИНСТИТУТ АВИАЦИИ, НАЗЕМНОГО ТРАНСПОРТА И ЭНЕРГЕТИКИ" 
        adress += "г. Казань, ул. Толстого, 15"
        phone += """+7 (843) 231 03 98, +7 (843) 231 03 20 (веч. отд.)"""
        mail += "iante@kai.ru"
        hours += """с 9:00 до 17:00 (дневное отделение)
с 15:00 до 19:00 (вечернее и заочное отделение)"""
        vkid += "iante_knrtu_kai" + " (Дирекция)"
        comm += "https://vk.me/join/AJQ1d/k1ehYuyfxfunfVwa8o"

        
    if header:
        mesg = header + "\n" + adress + phone + mail + hours + vkid + comm

    vk.method("messages.send",
                        {"peer_id": id, "message": mesg, "random_id": random.randint(1, 2147483647)})

    
      
    return "ok"



command = command_class.Command()




command.keys = ["институт", "деканат", "дирекция"]
command.desciption = ''
command.process = info
command.payload = "myinstitute"
