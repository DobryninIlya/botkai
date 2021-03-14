import json
# from user_class import UserParams
# from message_class import MessageSettings
import psycopg2
from .classes import MessageSettings, UserParams, connection, cursor
from pprint import pprint
import datetime

#######################################Keyboards#####################################################
exams_months = [1, 5, 6, 7, 8, 11, 12]


def get_button(label, color, payload="", type="text"):
    return {
        "action": {
            "type": type,
            "payload": json.dumps(payload),
            "label": label
        },
        "color": color
    }


def get_button_vkminiapp(app_id, owner_id, label, hash="", payload="", type="open_app"):
    return {
        "action": {
            "type": type,
            "app_id": app_id,
            "owner_id": owner_id,
            "payload": payload,
            "label": label,
            "hash": hash
        }
    }


def get_button_callback(label, color, payload=""):
    return {
        "action": {
            "type": "callback",
            "payload": json.dumps(payload),
            "label": label
        },
        "color": color
    }


def GetButtonTask(date):
    keyboard = {
        "inline": True,
        "buttons": [
            [get_button(label="Задания", color="positive", payload={'button': 'task', 'date': str(date)})]
        ]

    }
    keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
    keyboard = str(keyboard.decode('utf-8'))
    return keyboard


def GetButtonAnswer(id):
    keyboard = {
        "inline": True,
        "buttons": [
            [get_button(label="Ответить", color="positive", payload={'button': 'getanswer', 'id': str(id)})]
        ]

    }
    keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
    keyboard = str(keyboard.decode('utf-8'))
    return keyboard


def GetModerAdvButton(id):
    keyboard = {
        "inline": True,
        "buttons": [
            [get_button(label="Удалить", color="negative", payload={'button': 'deleteadv', 'id': str(id)}),
             get_button(label="Warn+delete", color="negative", payload={'button': 'deletewarnadv', 'id': str(id)}),
             get_button(label="След", color="negative", payload={'button': 'nextadv', 'id': str(id)})]
        ]

    }
    keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
    keyboard = str(keyboard.decode('utf-8'))
    return keyboard


def GetAdminPanel(level):
    buttons = []
    if level >= 5:
        buttons.append([get_button(label="moder nick", color="default", payload={'button': 'modernick'})])
        buttons.append([get_button(label="moder adv", color="default", payload={'button': 'moderadv'})])
        buttons.append([get_button(label="moder task", color="default", payload={'button': 'modertask'})])

        # buttons.append([get_button(label="moder storage", color="default", payload={'button': 'moderstorage'})])
        buttons.append([get_button(label="statistic", color="default", payload={'button': 'statistic'})])
    if level >= 20:
        buttons.append([get_button(label="reload", color="negative", payload={'button': 'reload'})])
        buttons.append([get_button(label="distribution", color="negative", payload={'button': 'admin_distr_all_info'})])

    buttons.append([get_button(label="Выход", color="default")])
    keyboard = {
        "one_time": False,
        "buttons": buttons

    }
    keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
    keyboard = str(keyboard.decode('utf-8'))
    return keyboard


def GetModerTaskButton(id):
    keyboard = {
        "inline": True,
        "buttons": [
            [get_button(label="Удалить", color="negative", payload={'button': 'deletetaskm', 'id': str(id)}),
             get_button(label="Warn+delete", color="negative", payload={'button': 'deletewarntask', 'id': str(id)}),
             get_button(label="След", color="negative", payload={'button': 'nexttask', 'id': str(id)})]
        ]

    }
    keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
    keyboard = str(keyboard.decode('utf-8'))
    return keyboard


def GetModerNickButton(id):
    keyboard = {
        "inline": True,
        "buttons": [
            [get_button(label="Удалить", color="negative", payload={'button': 'deletenick', 'id': str(id)}),
             get_button(label="Warn+delete", color="negative", payload={'button': 'deletewarnnick', 'id': str(id)}),
             get_button(label="След", color="negative", payload={'button': 'nextnick', 'id': str(id)})]
        ]

    }
    keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
    keyboard = str(keyboard.decode('utf-8'))
    return keyboard


def GetDeleteTaskButton(id):
    keyboard = {
        "inline": True,
        "buttons": [
            [get_button(label="Удалить задание", color="positive", payload={'button': 'deletetask', 'id': str(id)})]
        ]

    }
    keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
    keyboard = str(keyboard.decode('utf-8'))
    return keyboard


def GetModerStorageButton(id):
    keyboard = {
        "inline": True,
        "buttons": [
            [get_button(label="accept 5", color="positive", payload={'button': 'acceptstorage5', 'id': str(id)}),
             get_button(label="accept 15", color="positive", payload={'button': 'acceptstorage15', 'id': str(id)}),
             get_button(label="accept 45", color="positive", payload={'button': 'acceptstorage45', 'id': str(id)})],

            [get_button(label="accept 75", color="positive", payload={'button': 'acceptstorage75', 'id': str(id)}),
             get_button(label="Отказать и скрыть", color="negative", payload={'button': 'denystorage', 'id': str(id)})]
        ]

    }
    keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
    keyboard = str(keyboard.decode('utf-8'))
    return keyboard


def getdownloadstorage(id):
    keyboard = {
        "inline": True,
        "buttons": [
            [get_button(label="Скачать файл №" + str(id), color="primary",
                        payload={'button': 'downloadstorage', 'id': str(id)})]
        ]

    }
    keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
    keyboard = str(keyboard.decode('utf-8'))
    return keyboard


def GetModerTaskStarostaFirst(id, next_id, pos_id):
    buttons = [
        get_button(label="Удалить задание", color="negative", payload={'button': 'deletetask_starosta', 'id': str(id)},
                   type="callback")]
    if next_id != -1:
        buttons.append(get_button(label="Следующее", color="primary",
                                  payload={'button': 'next_task_starosta', 'id': str(next_id), "pos_id": pos_id,
                                           "type": "first"}, type="callback"))
    keyboard = {
        "inline": True,
        "buttons": [
            buttons
        ]

    }
    keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
    keyboard = str(keyboard.decode('utf-8'))
    return keyboard


def GetModerTaskStarosta(id, next_id, prev_id, pos_id):
    buttons = [get_button(label="Удалить задание", color="negative",
                          payload={'button': 'deletetask_starosta', 'id': str(id), "pos_id": pos_id}, type="callback")]
    if prev_id > 0:
        buttons.append(get_button(label="Предыдущее", color="primary",
                                  payload={'button': 'next_task_starosta', 'id': str(prev_id), "pos_id": pos_id,
                                           "type": "prev"}, type="callback"))

    if next_id != -1:
        buttons.append(get_button(label="Следующее", color="primary",
                                  payload={'button': 'next_task_starosta', 'id': str(next_id), "pos_id": pos_id,
                                           "type": "next"}, type="callback"))

    keyboard = {
        "inline": True,
        "buttons": [
            buttons
        ]

    }
    keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
    keyboard = str(keyboard.decode('utf-8'))
    return keyboard


keyboard = {
    "one_time": False,
    "buttons": [
        [get_button(label="Карантин, коронавирус...", color="negative", payload={'button': 'coronavirusfull'})],
        [
            get_button(label="На завтра", color="primary", payload={'button': 'tomorrow'}),
            get_button(label="Экзамены", color="positive", payload={'button': 'exams'})
        ],
        [
            get_button(label="На сегодня", color="primary", payload={'button': 'today'}),
            get_button(label="На послезавтра", color="primary", payload={'button': 'after'}),
            get_button(label="Полностью", color="primary", payload={'button': 'all'})
        ],
        [
            get_button(label="Четность недели", color="default", payload={'button': 'chetnost'}),
            get_button(label="Задания и объявления", color="primary", payload={'button': 'task menu'})
        ],
        [
            get_button(label="Команды", color="default", payload={'button': 'commands'}),
            get_button(label="Преподы", color="default", payload={'button': 'prepod'}),
            get_button(label="Хранилище", color="positive", payload={'button': 'storagemain'})
        ],
        [
            get_button(label="Обратная связь", color="primary", payload={'button': 'feedback'}),
            get_button(label="Профиль", color="positive", payload={'button': 'profile'})
        ]

    ]
}
keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
keyboard = str(keyboard.decode('utf-8'))


def getMainKeyboard(role):
    if role == 2:
        keyboard = {
            "one_time": False,
            "buttons": [
                [get_button(label="На завтра", color="positive", payload={'button': 'tomorrowprepod'})],
                [
                    get_button(label="На сегодня", color="primary", payload={'button': 'todayprepod'}),
                    get_button(label="На послезавтра", color="primary", payload={'button': 'afterprepod'}),
                    get_button(label="📄Полностью", color="primary", payload={'button': 'allprepod'})
                ],
                [
                    get_button(label="Четность недели", color="default", payload={'button': 'chetnost'}),
                    get_button(label="Обратная связь", color="primary", payload={'button': 'feedback'})
                ],
                [get_button(label="Другие действия", color="primary", payload={'button': 'prepod_submenu'})]
            ]
        }
        keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
        keyboard = str(keyboard.decode('utf-8'))
    elif role == 4:
        keyboard = {
            "one_time": False,
            "buttons": [
                [get_button(label="Про сервис", color="primary", payload={'button': 'infoabiturient'})],
                [{
                    "action": {
                        "type": "open_link",
                        "payload": json.dumps({"button": "official_site_link"}),
                        "label": "Официальный сайт",
                        "link": "https://abiturientu.kai.ru/"
                    }}],
                [{
                    "action": {
                        "type": "open_link",
                        "payload": json.dumps({"button": "official_vk_link"}),
                        "label": "Официальная группа ВКонтакте",
                        "link": "https://vk.com/kaiknitu"
                    }}],
                [get_button(label="Связь с админом", color="primary", payload={'button': 'feedback'})],
                [get_button(label="Пройти регистрацию заново", color="primary", payload={'button': 'undo_abiturient'})]
            ]
        }
        keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
        keyboard = str(keyboard.decode('utf-8'))
    elif role == 3:
        first_row = [get_button(label="🔔 На завтра", color="primary", payload={'button': 'tomorrow'}, type="text")]
        if datetime.date.today().month in exams_months:
            first_row.append(get_button(label="Экзамены", color="positive", payload={'button': 'exams'}, type="text"))
        keyboard = {
            "one_time": False,
            "buttons": [
                first_row,
                [
                    get_button(label="🔔 На сегодня", color="primary", payload={'button': 'today'}, type="text"),
                    get_button(label="🔔 На послезавтра", color="primary", payload={'button': 'after'}, type="text"),
                    get_button(label="📄Полностью", color="primary", payload={'button': 'all'}, type="text")
                ],
                [
                    get_button(label="🗓 Четность недели", color="default", payload={'button': 'chetnost'}, type="text")
                ],
                [
                    get_button(label="Команды", color="default", payload={'button': 'commands'}, type="text"),
                    get_button(label="👨‍🏫Преподы", color="default", payload={'button': 'prepod'}, type="text"),
                ],
                [
                    get_button(label="💌Обратная связь", color="primary", payload="{'button': 'feedback'}",
                               type="text"),
                    get_button(label="🔧Профиль", color="positive", payload={'button': 'profile'}, type="text")
                ]

            ]
        }
        keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
        keyboard = str(keyboard.decode('utf-8'))
    elif role == 5:
        keyboard = {
            "one_time": False,
            "buttons": [
                [get_button(label="Команды", color="primary", payload={'button': 'infoNitik'})]
            ]
        }
        keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
        keyboard = str(keyboard.decode('utf-8'))
    elif role == 6 and False:
        keyboard = {
            "one_time": False,
            "buttons": [
                [get_button(label="🔔 На завтра", color="primary", payload={'button': 'tomorrow'}, type="text")],
                [
                    get_button(label="📘 На сегодня", color="primary", payload={'button': 'today'}, type="text"),
                    get_button(label="📕 На послезавтра", color="primary", payload={'button': 'after'}, type="text"),
                    get_button(label="📄 На неделю", color="primary", payload={'button': 'week_shed_menu'},
                               type="text")],
                [
                    get_button(label="🗓 Четность недели", color="default", payload={'button': 'chetnost'},
                               type="text"),
                    get_button(label="📋 Задания и объявления", color="primary", payload={'button': 'task menu'},
                               type="text"),
                ],
                [
                    # get_button(label="📖 Разное", color="default", payload={'button': 'submenu'}, type="text"),
                    get_button(label="👨‍🏫 Преподы", color="default", payload={'button': 'prepod'}, type="text"),
                ],
                [
                    get_button(label="💌 Обратная связь", color="primary", payload={'button': 'feedback'}, type="text"),
                    get_button(label="👨🏻‍🎓 Профиль", color="positive", payload={'button': 'profile'}, type="text")
                ]

            ]
        }
        keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
        keyboard = str(keyboard.decode('utf-8'))
    else:
        first_row = [get_button(label="📗На завтра", color="primary", payload={'button': 'tomorrow'}, type="text")]
        if datetime.date.today().month in exams_months:
            first_row.append(get_button(label="Экзамены", color="positive", payload={'button': 'exams'}, type="text"))
        keyboard = {
            "one_time": False,
            "buttons": [
                first_row,
                [
                    get_button(label="📘 На сегодня", color="primary", payload={'button': 'today'}, type="text"),
                    get_button(label="📕 На послезавтра", color="primary", payload={'button': 'after'}, type="text"),
                    get_button(label="📄 На неделю", color="primary", payload={'button': 'week_shed_menu'},
                               type="text")],
                [
                    get_button(label="🗓 Четность недели", color="default", payload={'button': 'chetnost'},
                               type="text"),
                    get_button(label="📋 Задания и объявления", color="primary", payload={'button': 'task menu'},
                               type="text"),
                ],
                [
                    get_button(label="📖 Разное", color="default", payload={'button': 'submenu'}, type="text"),
                    get_button(label="👨‍🏫 Преподы", color="default", payload={'button': 'prepod'}, type="text"),
                ],
                [
                    get_button(label="💌 Обратная связь", color="primary", payload={'button': 'feedback'}, type="text"),
                    get_button(label="👨🏻‍🎓 Профиль", color="positive", payload={'button': 'profile'}, type="text")
                ]

            ]
        }
        keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
        keyboard = str(keyboard.decode('utf-8'))
    return keyboard


def KeyboardProfile():
    if UserParams.role != 3:
        Name = UserParams.name
        keys = ["на завтра", "на сегодня", "команды", "помощь", 'начать', 'расписание']
        NameColor = "default"
        if Name.lower() in keys:
            Name = "Некорректно. Нажми, чтобы обновить"
            NameColor = "negative"
        Group = UserParams.RealGroup
        GroupColor = "default"
        inst = ""
        if Group == 0:
            Group = "Не указано. Нажми, чтобы указать"
            GroupColor = "negative"
            inst = ":Не указана группа"
        Balance = UserParams.balance
        sql = "SELECT COUNT(*) FROM Task WHERE UserID = " + str(MessageSettings.getId())
        cursor.execute(sql)
        TaskCount = cursor.fetchone()[0]
        main_buttons = [[get_button(label="Имя: " + Name[:30], color="positive", payload={'button': 'name'})],

                        [get_button(label="Группа: " + str(Group), color=GroupColor, payload={'button': 'group'})],
                        [get_button(label="Баланс: " + str(Balance), color="positive", payload={'button': 'donate'})],
                        [get_button(label="Мои задания (" + str(TaskCount) + ")", color="default",
                                    payload={'button': 'mytask'})],
                        [
                            get_button(label="Полный список группы", color="default",
                                       payload={'button': 'groupmembersall'}),
                            get_button(label="Моя группа", color="default", payload={'button': 'groupmembers'})
                        ],
                        [
                            get_button(label="Мой институт " + inst, color=GroupColor,
                                       payload={'button': 'myinstitute'}),
                            get_button(label="Подписки", color="default", payload={'button': 'distrMenu'})
                        ],
                        ]
        if UserParams.role == 6 and False:
            main_buttons[-1].remove(main_buttons[-1][-1])
        sql = "SELECT COUNT(*) FROM users WHERE users.groupp = {} AND admLevel = 2".format(UserParams.groupId)
        cursor.execute(sql)
        starosta_count = cursor.fetchone()[0]
        if int(starosta_count) == 0:
            main_buttons.append([get_button(label="Староста не назначен. Стать им", color="positive",
                                            payload={'button': 'get_starosta'})])
        if UserParams.adminLevel >= 2:
            main_buttons.append(
                [get_button(label="Меню старосты", color="default", payload={'button': 'starosta_menu'})])

        if UserParams.own_shed and UserParams.role != 6:
            main_buttons.append([get_button(label="Использовать свое расписание", color="positive",
                                            payload={'button': 'select_own_shedule'})])
        elif UserParams.role != 6:
            main_buttons.append([get_button(label="Использовать расписание группы", color="default",
                                            payload={'button': 'select_own_shedule'})])

        main_buttons.append([get_button(label="Назад", color="default", payload={'button': 'tomainmenu'})])

        keyboard = {
            "one_time": False,
            "buttons": main_buttons
        }
        keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
        keyboard = str(keyboard.decode('utf-8'))
        return keyboard
    else:
        Name = UserParams.name
        keys = ["на завтра", "на сегодня", "команды", "помощь", 'начать', 'расписание']
        NameColor = "default"
        if Name.lower() in keys:
            Name = "Некорректно. Нажми, чтобы обновить"
            NameColor = "negative"
        Group = UserParams.RealGroup
        GroupColor = "default"
        inst = ""
        if Group == 0:
            Group = "Не указано. Нажми, чтобы указать"
            GroupColor = "negative"
            inst = ":Не указана группа"
        Balance = UserParams.balance

        main_buttons = [[get_button(label="Имя: " + Name[:30], color="positive", payload={'button': 'name'})], [
            get_button(label="(Родитель) Группа: " + str(Group), color=GroupColor, payload={'button': 'group'})],
                        [get_button(label="Баланс: " + str(Balance), color="positive", payload={'button': 'donate'})], [
                            get_button(label="Список родителей группы", color="default",
                                       payload={'button': 'groupmembers'})],
                        [get_button(label="Мой институт " + inst, color=GroupColor, payload={'button': 'myinstitute'})],
                        [get_button(label="Назад", color="default", payload={'button': 'tomainmenu'})]]

        keyboard = {
            "one_time": False,
            "buttons": main_buttons
        }
        keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
        keyboard = str(keyboard.decode('utf-8'))
        return keyboard


def GetStarostaKeyboard(first=0):
    buttons_starosta = []
    if UserParams.adminLevel >= 2 or first:
        buttons_starosta = [
            [get_button(label="Загрзка расписания из Excel", color="default", payload={'button': 'starostaexcel'})],
            [get_button(label="Проверка заданий", color="default", payload={'button': 'starostatask'})],
            [get_button(label="Удаление объявлений", color="default", payload={'button': 'starosta_adv_delete'})],
            [get_button(label="Принудительное обновление расписания", color="default",
                        payload={'button': 'starosta_shed_update_info'})],
            [get_button(label="Выдать предупреждение", color="default", payload={'button': 'starosta_warn_info'})],
            [get_button(label="Кикнуть из группы", color="default", payload={'button': 'starosta_kick_info'})],
            [get_button(label="Сделать рассылку", color="default", payload={'button': 'starosta_distr_info'})],
            [get_button(label="Перестать быть старостой", color="negative", payload={'button': 'starosta_leave'})],
            [get_button(label="Назад", color="primary", payload={'button': 'profile'})],
        ]

    keyboard = {
        "one_time": False,
        "buttons": buttons_starosta
    }
    keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
    keyboard = str(keyboard.decode('utf-8'))
    return keyboard


def GetButtonDeleteByDate():
    today = datetime.date.today()
    today_date = today.strftime("%d.%m")
    today += datetime.timedelta(days=1)
    tomorrow_date = today.strftime("%d.%m")
    today += datetime.timedelta(days=1)
    after_date = today.strftime("%d.%m")
    keyboard = {
        "one_time": False,
        "buttons": [
            [
                get_button(label=today_date, color="default"),
                get_button(label=tomorrow_date, color="default"),
                get_button(label=after_date, color="default")
            ],
            [get_button(label="Выход", color="negative")]
        ]

    }
    keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
    keyboard = str(keyboard.decode('utf-8'))
    return keyboard


week_shed_kbrd = {
    "one_time": False,
    "buttons": [
        [
            get_button(label="Понедельник", color="default", payload={'button': 'week_shed', 'day': 1}),
            get_button(label="Вторник", color="default", payload={'button': 'week_shed', 'day': 2}),
            get_button(label="Среда", color="default", payload={'button': 'week_shed', 'day': 3})
        ],
        [
            get_button(label="Четверг", color="default", payload={'button': 'week_shed', 'day': 4}),
            get_button(label="Пятница", color="default", payload={'button': 'week_shed', 'day': 5}),
            get_button(label="Суббота", color="default", payload={'button': 'week_shed', 'day': 6})
        ],
        [get_button(label="Полностью", color="default", payload={'button': 'all'})],
        [get_button(label="Назад", color="negative", payload={'button': 'tomainmenu'})],
    ]

}
week_shed_kbrd = json.dumps(week_shed_kbrd, ensure_ascii=False).encode('utf-8')
week_shed_kbrd = str(week_shed_kbrd.decode('utf-8'))

make_admin_distr = {
    "inline": True,
    "buttons": [
        [get_button(label="Разослать сообщение admin", color="negative", payload={'button': 'make_admin_distr'})]
    ]

}
make_admin_distr = json.dumps(make_admin_distr, ensure_ascii=False).encode('utf-8')
make_admin_distr = str(make_admin_distr.decode('utf-8'))

make_distr = {
    "inline": True,
    "buttons": [
        [get_button(label="Разослать сообщение", color="primary", payload={'button': 'make_distr'})]
    ]

}
make_distr = json.dumps(make_distr, ensure_ascii=False).encode('utf-8')
make_distr = str(make_distr.decode('utf-8'))

shed_update = {
    "inline": True,
    "buttons": [
        [get_button(label="Обновить расписание в бд", color="primary", payload={'button': 'shed_update'})]
    ]

}
shed_update = json.dumps(shed_update, ensure_ascii=False).encode('utf-8')
shed_update = str(shed_update.decode('utf-8'))

get_undo = {
    "inline": False,
    "buttons": [
        [get_button(label="Назад", color="negative", payload={'button': 'undo_regestration'})]
    ]

}
get_undo = json.dumps(get_undo, ensure_ascii=False).encode('utf-8')
get_undo = str(get_undo.decode('utf-8'))

make_warn = {
    "inline": True,
    "buttons": [
        [get_button(label="Выдать предупреждение", color="primary", payload={'button': 'make_warn'})]
    ]

}
make_warn = json.dumps(make_warn, ensure_ascii=False).encode('utf-8')
make_warn = str(make_warn.decode('utf-8'))

make_kick = {
    "inline": True,
    "buttons": [
        [get_button(label="Кикнуть из группы", color="primary", payload={'button': 'make_kick'})]
    ]

}
make_kick = json.dumps(make_kick, ensure_ascii=False).encode('utf-8')
make_kick = str(make_kick.decode('utf-8'))

make_starosta = {
    "inline": True,
    "buttons": [
        [get_button(label="Стать старостой", color="primary", payload={'button': 'make_starosta'})]
    ]

}
make_starosta = json.dumps(make_starosta, ensure_ascii=False).encode('utf-8')
make_starosta = str(make_starosta.decode('utf-8'))

coronavirus = {
    "inline": True,
    "buttons": [
        [get_button(label="Подробнее...", color="negative", payload={'button': 'coronavirusfull'})]
    ]

}
coronavirus = json.dumps(coronavirus, ensure_ascii=False).encode('utf-8')
coronavirus = str(coronavirus.decode('utf-8'))

coronavirusfull = {
    "one_time": False,
    "buttons": [
        [get_button(label="О карантине", color="positive", payload={'button': 'aboutcoronavirus'})],
        [get_button(label="Меры предосторожности", color="primary", payload={'button': 'safety'})],
        [get_button(label="Чем заняться дома", color="primary", payload={'button': 'homechill'})],
        [get_button(label="Выход", color="negative")]

    ]

}
coronavirusfull = json.dumps(coronavirusfull, ensure_ascii=False).encode('utf-8')
coronavirusfull = str(coronavirusfull.decode('utf-8'))

gamehub = {
    "one_time": False,
    "buttons": [
        [get_button(label="Мафия", color="positive", payload={'button': 'mafiahub'})],
        [get_button(label="Выход", color="negative")]

    ]

}
gamehub = json.dumps(gamehub, ensure_ascii=False).encode('utf-8')
gamehub = str(gamehub.decode('utf-8'))

mafiahub = {
    "one_time": False,
    "buttons": [
        [get_button(label="Как играть", color="positive", payload={'button': 'mafiahub'})],
        [get_button(label="Создать комнату", color="positive", payload={'button': 'mafiaroomadd'})],
        [get_button(label="Список комнат", color="positive", payload={'button': 'mafiaroomlist'})],
        [get_button(label="Подключиться к игре", color="positive", payload={'button': 'mafiainvite'})],
        [get_button(label="Назад", color="negative", payload={'button': 'gamehub'})]

    ]

}
mafiahub = json.dumps(mafiahub, ensure_ascii=False).encode('utf-8')
mafiahub = str(mafiahub.decode('utf-8'))

roleMenu = {
    "one_time": True,
    "buttons": [
        [get_button(label="Абитуриент (поступающий)", color="positive")],
        [get_button(label="Студент", color="positive")],
        [get_button(label="Преподаватель", color="primary")],
        [get_button(label="Родитель", color="primary")],
        [get_button(label="Справка", color="negative")]

    ]

}
roleMenu = json.dumps(roleMenu, ensure_ascii=False).encode('utf-8')
roleMenu = str(roleMenu.decode('utf-8'))

warnList = {
    "inline": True,
    "buttons": [
        [get_button(label="Просмотреть предупреждения", color="default", payload={'button': 'warnlist'})]

    ]
}
warnList = json.dumps(warnList, ensure_ascii=False).encode('utf-8')
warnList = str(warnList.decode('utf-8'))

warnInfo = {
    "inline": True,
    "buttons": [
        [get_button(label="Что это такое?", color="primary", payload={'button': 'warnInfo'})]

    ]
}
warnInfo = json.dumps(warnInfo, ensure_ascii=False).encode('utf-8')
warnInfo = str(warnInfo.decode('utf-8'))

keyboardRef = {
    "one_time": False,
    "buttons": [
        [get_button(label="Справка", color="primary")],
        [get_button(label="Продолжить регистрацию", color="positive")]

    ]
}
keyboardRef = json.dumps(keyboardRef, ensure_ascii=False).encode('utf-8')
keyboardRef = str(keyboardRef.decode('utf-8'))

keyboardRef1 = {
    "one_time": False,
    "buttons": [
        [get_button(label="Позвать", color="primary")],
        [get_button(label="Продолжить регистрацию", color="positive")]

    ]
}
keyboardRef1 = json.dumps(keyboardRef1, ensure_ascii=False).encode('utf-8')
keyboardRef1 = str(keyboardRef1.decode('utf-8'))

keyboardAddTasks = {
    "one_time": False,
    "buttons": [
        [
            get_button(label="Через неделю", color="primary"),
            get_button(label="Через 2 недели", color="primary")
        ],
        [get_button(label="Выход", color="default")]

    ]
}
keyboardAddTasks = json.dumps(keyboardAddTasks, ensure_ascii=False).encode('utf-8')
keyboardAddTasks = str(keyboardAddTasks.decode('utf-8'))

keyboardAddTasks2 = {
    "one_time": True,
    "buttons": [

        [get_button(label="Выход", color="negative")]

    ]
}
keyboardAddTasks2 = json.dumps(keyboardAddTasks2, ensure_ascii=False).encode('utf-8')
keyboardAddTasks2 = str(keyboardAddTasks2.decode('utf-8'))

exit = {
    "one_time": False,
    "buttons": [

        [get_button(label="Выход", color="negative")]

    ]
}
exit = json.dumps(exit, ensure_ascii=False).encode('utf-8')
exit = str(exit.decode('utf-8'))

AModerationTask = {
    "one_time": False,
    "buttons": [
        [
            get_button(label="Подтвердить", color="positive", payload={'button': 'confirm task'}),
            get_button(label="Удалить", color="positive", payload={'button': 'delete task'}),
        ],

        [get_button(label="Назад", color="negative")]

    ]
}
AModerationTask = json.dumps(AModerationTask, ensure_ascii=False).encode('utf-8')
AModerationTask = str(AModerationTask.decode('utf-8'))

AdminPanel = {
    "one_time": False,
    "buttons": [
        [get_button(label="Статистика", color="positive", payload={'button': 'statistic'})],
        [get_button(label="Начать модерацию заданий", color="default", payload={'button': 'task moderation'})],
        [get_button(label="Начать модерацию заметок", color="default", payload={'button': 'notes moderation'})],
        [get_button(label="Начать модерацию ников", color="default", payload={'button': 'nick moderation'})],
        [get_button(label="Перезагрузка", color="default", payload={'button': 'nick moderation'})],
        [get_button(label="Назад", color="negative")]

    ]
}
AdminPanel = json.dumps(AdminPanel, ensure_ascii=False).encode('utf-8')
AdminPanel = str(AdminPanel.decode('utf-8'))

keyboardTasks = {
    "one_time": False,
    "buttons": [
        [get_button(label="Добавить задание", color="positive", payload={'button': 'add task'}),
         get_button(label="Добавить объявление", color="positive", payload={'button': 'add ad'})],
        [get_button(label="На завтра", color="default", payload={'button': 'task', 'date': 'tomorrow'})],
        [
            get_button(label="На сегодня", color="primary", payload={'button': 'task', 'date': 'today'}),
            get_button(label="На послезавтра", color="primary", payload={'button': 'task', 'date': 'after'}),

        ],
        [get_button(label="Назад", color="negative")]

    ]
}
keyboardTasks = json.dumps(keyboardTasks, ensure_ascii=False).encode('utf-8')
keyboardTasks = str(keyboardTasks.decode('utf-8'))

keyboardGroupChat = {
    # "one_time": True,
    "buttons": [
        [get_button(label="На завтра", color="positive")],
        [
            get_button(label="На сегодня", color="primary"),
            get_button(label="На послезавтра", color="primary"),

        ]

    ],
    "inline": True

}
keyboardGroupChat = json.dumps(keyboardGroupChat, ensure_ascii=False).encode('utf-8')
keyboardGroupChat = str(keyboardGroupChat.decode('utf-8'))

storageMain = {
    "one_time": True,
    "buttons": [
        [get_button(label="Что это такое? Как пользоваться?", color="positive", payload={'button': 'storageinfo'})],
        [get_button(label="Добавить файл", color="default", payload={'button': 'storageadd'})],
        [get_button(label="Мои файлы", color="default", payload={'button': 'mystoragelist'})],
        [get_button(label="Поиск по базе", color="default", payload={'button': 'searchstorage'})],
        [get_button(label="Просмотреть файл", color="default", payload={'button': 'storagedownload'})],
        [get_button(label="Выход", color="negative")],

    ],

}
storageMain = json.dumps(storageMain, ensure_ascii=False).encode('utf-8')
storageMain = str(storageMain.decode('utf-8'))

keyboardNull = {
    "one_time": True,
    "buttons": [

    ]  # ,
    # "inline" : True

}
keyboardNull = json.dumps(keyboardNull, ensure_ascii=False).encode('utf-8')
keyboardNull = str(keyboardNull.decode('utf-8'))

keyboardContinio = {
    "one_time": True,
    "buttons": [

        [get_button(label="Продолжить", color="positive")],
        [get_button(label="Выход", color="negative")]

    ]
}
keyboardContinio = json.dumps(keyboardContinio, ensure_ascii=False).encode('utf-8')
keyboardContinio = str(keyboardContinio.decode('utf-8'))

keyboardWeekday = {
    "one_time": True,
    "buttons": [

        [get_button(label="Понедельник", color="default")],
        [get_button(label="Вторник", color="default")],
        [get_button(label="Среда", color="default")],
        [get_button(label="Четверг", color="default")],
        [get_button(label="Воскресенье", color="default")],
        [get_button(label="Пятница", color="default")],
        [get_button(label="Суббота", color="default")],

    ]
}
keyboardWeekday = json.dumps(keyboardWeekday, ensure_ascii=False).encode('utf-8')
keyboardWeekday = str(keyboardWeekday.decode('utf-8'))

keyboardweather = {
    "one_time": False,
    "buttons": [

        [get_button(label="Сегодня", color="positive")],
        [get_button(label="На 5 дней", color="primary")],
        [get_button(label="Назад", color="default")]
    ]
}
keyboardweather = json.dumps(keyboardweather, ensure_ascii=False).encode('utf-8')
keyboardweather = str(keyboardweather.decode('utf-8'))

keyboard2 = {
    "one_time": False,
    "buttons": [
        [get_button(label="Услуги", color="positive")],
        [get_button(label="Информация", color="primary")],
        [get_button(label="Заметки", color="primary")],
        [get_button(label="Пожертвовать $", color="positive")],
        [get_button(label="Погода", color="primary")],
        [get_button(label="<- <- <-", color="default")]

    ]
}
keyboard2 = json.dumps(keyboard2, ensure_ascii=False).encode('utf-8')
keyboard2 = str(keyboard2.decode('utf-8'))

keyboardInfo = {
    "one_time": False,
    "buttons": [

        [get_button(label="Институты", color="primary")],
        [get_button(label="Здания", color="primary")],
        [get_button(label="Электронные учебники/методички/пособия", color="primary")],
        [get_button(label="Назад", color="default")]

    ]
}
keyboardInfo = json.dumps(keyboardInfo, ensure_ascii=False).encode('utf-8')
keyboardInfo = str(keyboardInfo.decode('utf-8'))

keyboardNotes = {
    "one_time": False,
    "buttons": [

        [get_button(label="Все заметки", color="positive")],
        [
            get_button(label="Понедельник заметка", color="primary"),
            get_button(label="Вторник заметка", color="primary"),
            get_button(label="Среда заметка", color="primary"),
        ],
        [
            get_button(label="Четверг заметка", color="primary"),
            get_button(label="Пятница заметка", color="primary"),
            get_button(label="Суббота заметка", color="primary"),
        ],
        [get_button(label="Воскресенье заметка", color="primary")],
        [get_button(label="Добавить заметку", color="positive")],
        [get_button(label="Выход", color="default")]

    ]
}
keyboardNotes = json.dumps(keyboardNotes, ensure_ascii=False).encode('utf-8')
keyboardNotes = str(keyboardNotes.decode('utf-8'))

keyboardAddOrChange = {
    "one_time": True,
    "buttons": [

        [get_button(label="Добавить", color="primary")],
        [get_button(label="Заменить", color="primary")]

    ]
}
keyboardAddOrChange = json.dumps(keyboardAddOrChange, ensure_ascii=False).encode('utf-8')
keyboardAddOrChange = str(keyboardAddOrChange.decode('utf-8'))

keyboarddonate = {
    "one_time": False,
    "buttons": [

        [{"action": {"type": "vkpay", "hash": "action=transfer-to-group&group_id=182372147&aid=10"}}],
        [get_button(label="Назад", color="default")]

    ]
}
keyboarddonate = json.dumps(keyboarddonate, ensure_ascii=False).encode('utf-8')
keyboarddonate = str(keyboarddonate.decode('utf-8'))

mafia_acceptgame = {
    "one_time": False,
    "buttons": [
        [get_button(label="Готов!", color="positive", payload={'button': 'mafiaacceptgame'})]
    ]

}
mafia_acceptgame = json.dumps(mafia_acceptgame, ensure_ascii=False).encode('utf-8')
mafia_acceptgame = str(mafia_acceptgame.decode('utf-8'))

testButtons = {
    "inline": True,
    "buttons": [
        [get_button(label="test buttons", color="negative", payload={}),
         get_button(label="test buttons", color="negative", payload={}),
         get_button(label="test buttons", color="negative", payload={}),
         get_button(label="test buttons", color="negative", payload={}),
         get_button(label="test buttons", color="negative", payload={})],
        [get_button(label="test buttons", color="negative", payload={}),
         get_button(label="test buttons", color="negative", payload={}),
         get_button(label="test buttons", color="negative", payload={})],
        [get_button(label="test buttons", color="negative", payload={}),
         get_button(label="test buttons", color="negative", payload={}),
         get_button(label="test buttons", color="negative", payload={})]
    ]

}
testButtons = json.dumps(testButtons, ensure_ascii=False).encode('utf-8')
testButtons = str(testButtons.decode('utf-8'))

help_starosta_upload = {
    "inline": True,
    "buttons": [
        [get_button_vkminiapp(label="Гайд", app_id='7505621', owner_id="182372147", hash="starosta")]

    ]

}
help_starosta_upload = json.dumps(help_starosta_upload, ensure_ascii=False).encode('utf-8')
help_starosta_upload = str(help_starosta_upload.decode('utf-8'))

help_starosta_affiliate = {
    "inline": True,
    "buttons": [
        [get_button_vkminiapp(label="Гайд по настройке расписания", app_id='7505621', owner_id="182372147",
                              hash="affiliate")]

    ]

}
help_starosta_affiliate = json.dumps(help_starosta_affiliate, ensure_ascii=False).encode('utf-8')
help_starosta_affiliate = str(help_starosta_affiliate.decode('utf-8'))

submenu = {
    "inline": False,
    "buttons": [
        [get_button_vkminiapp(label="Графическая справка", app_id='7505621', owner_id="182372147")],
        [get_button(label="Здания", color="default", payload={'button': 'buildings_menu'})],
        [get_button(label="Команды", color="default", payload={'button': 'commands'})],
        [get_button(label="Экспорт расписания в .docx", color="default", payload={'button': 'exportword'})],
        [get_button(label="Экспорт расписания в .ics (.ical)", color="default", payload={'button': 'exportcalendar'})],
        [get_button(label="Активности", color="default", payload={'button': 'activities'})],
        [get_button(label="Назад", color="default", payload={})]

    ]

}
submenu = json.dumps(submenu, ensure_ascii=False).encode('utf-8')
submenu = str(submenu.decode('utf-8'))

buildings_menu = {
    "inline": False,
    "buttons": [

        [get_button(label="1", color="primary", payload={'button': 'buildings_num', 'number': 1}),
         get_button(label="2", color="primary", payload={'button': 'buildings_num', 'number': 2}),
         get_button(label="3", color="primary", payload={'button': 'buildings_num', 'number': 3}),
         get_button(label="4", color="primary", payload={'button': 'buildings_num', 'number': 4})
         ],
        [get_button(label="5", color="primary", payload={'button': 'buildings_num', 'number': 5}),
         get_button(label="6", color="primary", payload={'button': 'buildings_num', 'number': 6}),
         get_button(label="7", color="primary", payload={'button': 'buildings_num', 'number': 7}),
         get_button(label="8", color="primary", payload={'button': 'buildings_num', 'number': 8})
         ],
        [get_button(label="Назад", color="default", payload={})]

    ]

}
buildings_menu = json.dumps(buildings_menu, ensure_ascii=False).encode('utf-8')
buildings_menu = str(buildings_menu.decode('utf-8'))

keyboardPrepodSubmenu = {
    "one_time": False,
    "buttons": [
        # [get_button(label="Сообщение студентам", color="primary")],
        [get_button(label="Сообщение студентам", payload={'button': "prepod_share_message_info"}, color="primary")],
        [get_button(label="Объявление студентам по дате", color="primary")],
        [get_button(label="Задание студентам по дате", color="primary")],
        [get_button(label="Собственное расписание", color="primary")],
        [get_button(label="Выход", color="negative")]
    ]

}
keyboardPrepodSubmenu = json.dumps(keyboardPrepodSubmenu, ensure_ascii=False).encode('utf-8')
keyboardPrepodSubmenu = str(keyboardPrepodSubmenu.decode('utf-8'))

keyboardPrepodShareMessage = {
    "one_time": False,
    'inline' : True,
    "buttons": [
        [get_button(label="Продолжить", payload={'button': "prepod_share_message_next"}, color="positive")]
    ]

}
keyboardPrepodShareMessage = json.dumps(keyboardPrepodShareMessage, ensure_ascii=False).encode('utf-8')
keyboardPrepodShareMessage = str(keyboardPrepodShareMessage.decode('utf-8'))

#######################################Keyboards#####################################################
