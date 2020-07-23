import json
#from user_class import UserParams
#from message_class import MessageSettings
import psycopg2
from .classes import MessageSettings, UserParams
from pprint import pprint
#######################################Keyboards#####################################################


def get_button(label, color, payload="", type = "text"):
    return {
        "action": {
            "type": type,
            "payload": json.dumps(payload),
            "label": label
        },
        "color": color
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
            [get_button(label="Задания", color="positive", payload = {'button': 'task', 'date' : str(date)})]
            ]
            
    }
    keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
    keyboard = str(keyboard.decode('utf-8'))
    return keyboard


def GetButtonAnswer(id):

    keyboard = {
        "inline": True,
        "buttons": [
            [get_button(label="Ответить", color="positive", payload = {'button': 'getanswer', 'id' : str(id) })]
            ]
            
    }
    keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
    keyboard = str(keyboard.decode('utf-8'))
    return keyboard

def GetModerAdvButton(id):

    keyboard = {
        "inline": True,
        "buttons": [
            [get_button(label="Удалить", color="negative", payload = {'button': 'deleteadv', 'id' : str(id)}),
             get_button(label="Warn+delete", color="negative", payload = {'button': 'deletewarnadv', 'id' : str(id)}),
             get_button(label="След", color="negative", payload = {'button': 'nextadv', 'id' : str(id)})]
            ]
            
    }
    keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
    keyboard = str(keyboard.decode('utf-8'))
    return keyboard


def GetAdminPanel(level):
    buttons = []
    if level>=5:
        buttons.append([get_button(label="moder nick", color="default", payload={'button': 'modernick'})])
        buttons.append([get_button(label="moder adv", color="default", payload={'button': 'moderadv'})])
        buttons.append([get_button(label="moder task", color="default", payload={'button': 'modertask'})])
        buttons.append([get_button(label="moder storage", color="default", payload={'button': 'moderstorage'})])
        buttons.append([get_button(label="Statistic", color="default", payload={'button': 'statistic'})])
    if level >= 20:
        buttons.append([get_button(label="reload", color="negative", payload={'button': 'reload'})])

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
            [get_button(label="Удалить задание", color="positive", payload = {'button': 'deletetask', 'id' : str(id)})]
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
            [get_button(label="Скачать файл №" + str(id), color="primary", payload={'button': 'downloadstorage', 'id': str(id)})]
        ]

    }
    keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
    keyboard = str(keyboard.decode('utf-8'))
    return keyboard


keyboard = {
    "one_time": False,
    "buttons": [
        [get_button(label="Карантин, коронавирус...", color="negative", payload = {'button': 'coronavirusfull'})],
        [
            get_button(label="На завтра", color="primary", payload = {'button': 'tomorrow'}),
            get_button(label="Экзамены", color="positive", payload = {'button': 'exams'})
                ],
        [
            get_button(label="На сегодня", color="primary", payload = {'button': 'today'}),
            get_button(label="На послезавтра", color="primary", payload = {'button': 'after'}),
            get_button(label="Полностью", color="primary", payload = {'button': 'all'})
            ],
        [
            get_button(label="Четность недели", color="default", payload = {'button': 'chetnost'}),
            get_button(label="Задания и объявления", color="primary", payload = {'button': 'task menu'})
         ],
        [
            get_button(label="Команды", color="default", payload = {'button': 'commands'}),
            get_button(label="Преподы", color="default", payload = {'button': 'prepod'}),
            get_button(label="Хранилище", color="positive", payload = {'button': 'storagemain'})
            ],
        [
            get_button(label="Обратная связь", color="primary", payload = {'button': 'feedback'}),
            get_button(label="Профиль", color="positive", payload = {'button': 'profile'})
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
            [get_button(label="На завтра", color="positive", payload = {'button': 'tomorrowprepod'})],
            [
                get_button(label="На сегодня", color="primary", payload = {'button': 'todayprepod'}),
                get_button(label="На послезавтра", color="primary", payload = {'button': 'afterprepod'}),
                get_button(label="Полностью", color="primary", payload = {'button': 'allprepod'})
                ],
            [
                get_button(label="Четность недели", color="default", payload = {'button': 'chetnost'}),
                get_button(label="Обратная связь", color="primary", payload = {'button': 'feedback'})
                ]


            ]
            }
        keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
        keyboard = str(keyboard.decode('utf-8'))
    elif role == 4:
        keyboard = {
            "one_time": False,
            "buttons": [
                [get_button(label="Про сервис", color="primary", payload = {'button': 'infoabiturient'})],
                    [{
                "action": {
                    "type": "open_link",
                    "payload": json.dumps({"button" : "official_site_link"}),
                    "label": "Официальный сайт",
                    "link" : "https://abiturientu.kai.ru/"
                }}],
                [{
                "action": {
                    "type": "open_link",
                    "payload": json.dumps({"button" :"official_vk_link"}),
                    "label": "Официальная группа ВКонтакте",
                    "link" : "https://vk.com/kaiknitu"
                }}],
                [get_button(label="Связь с админом", color="primary", payload = {'button': 'feedback'})]
            ]
            }
        keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
        keyboard = str(keyboard.decode('utf-8'))
    elif role == 5:
        keyboard = {
            "one_time": False,
            "buttons": [
                [get_button(label="Команды", color="primary", payload = {'button': 'infoNitik'})]
            ]   
            }
        keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
        keyboard = str(keyboard.decode('utf-8'))
    else:
        keyboard = {
            "one_time": False,
            "buttons": [
            #[get_button(label="Карантин, коронавирус...", color="negative", payload = {'button': 'coronavirusfull'})],
            [
                get_button(label="На завтра", color="primary", payload = {'button': 'tomorrow'}, type = "text"),
                get_button(label="Экзамены", color="positive", payload = {'button': 'exams'}, type = "text")],
            [
                get_button(label="На сегодня", color="primary", payload = {'button': 'today'}, type = "text"),
                get_button(label="На послезавтра", color="primary", payload = {'button': 'after'}, type = "text"),
                get_button(label="Полностью", color="primary", payload = {'button': 'all'}, type = "text")
                ],
            [
                get_button(label="Четность недели", color="default", payload = {'button': 'chetnost'}, type = "text"),
                get_button(label="Задания и объявления", color="primary", payload = {'button': 'task menu'}, type = "text"),
                get_button(label="Мини-игры", color="default", payload = {'button': 'gamehub'}, type = "text"),
                ],
            [
                get_button(label="Команды", color="default", payload = {'button': 'commands'}, type = "text"),
                get_button(label="Преподы", color="default", payload = {'button': 'prepod'}, type = "text"),
                get_button(label="Хранилище", color="positive", payload = {'button': 'storagemain'}, type = "text")
                ],
            [
                get_button(label="Обратная связь", color="primary", payload = "{'button': 'feedback'}", type = "text"),
                get_button(label="Профиль", color="positive", payload = "{'button': 'profile'}", type = "text")
                ]


            ]
            }
        keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
        keyboard = str(keyboard.decode('utf-8'))
        #pprint(keyboard)
    return keyboard



def KeyboardProfile():
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
    connection = psycopg2.connect(dbname='dfdn09mdk3r1gr', user='olkywigpsefwye', password='6f73707c0610067f60ed525f472fcbc34e3af291dbc21e6bec1d6d3ed89c94b9', host='ec2-54-246-121-32.eu-west-1.compute.amazonaws.com')
    cursor = connection.cursor()
    sql = "SELECT COUNT(*) FROM Task WHERE UserID = " + str(MessageSettings.getId())
    cursor.execute(sql)
    TaskCount = cursor.fetchone()[0]
    connection.close()
    
    keyboard =  {
    "one_time": False,
    "buttons": [
        [get_button(label="Имя: " + Name[:30], color="positive", payload = {'button': 'name'})],

        [get_button(label="Группа: " + str(Group), color=GroupColor, payload = {'button': 'group'})],
        [get_button(label="Баланс: " + str(Balance), color="positive", payload = {'button': 'donate'})],
        [get_button(label="Мои задания (" + str(TaskCount) + ")", color="default", payload = {'button': 'mytask'})],
        [get_button(label="Список моей группы", color="default", payload = {'button': 'groupmembers'})],
        [
            get_button(label="Мой институт " + inst, color=GroupColor, payload = {'button': 'myinstitute'}),
            get_button(label="Подписки", color = "default", payload = {'button': 'distrMenu'})
            ],
        [get_button(label="Назад", color="default", payload = {'button': 'tomainmenu'})]


        ]
    }
    keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
    keyboard = str(keyboard.decode('utf-8'))
    return keyboard


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
        [get_button(label="О карантине", color="positive", payload = {'button': 'aboutcoronavirus'})],
        [get_button(label="Меры предосторожности", color="primary", payload = {'button': 'safety'})],
        [get_button(label="Чем заняться дома", color="primary", payload = {'button': 'homechill'})],
        [get_button(label="Выход", color="negative")]


    ]

}
coronavirusfull = json.dumps(coronavirusfull, ensure_ascii=False).encode('utf-8')
coronavirusfull = str(coronavirusfull.decode('utf-8'))


gamehub = {
    "one_time": False,
    "buttons": [
        [get_button(label="Мафия", color="positive", payload = {'button': 'mafiahub'})],
        [get_button(label="Выход", color="negative")]


    ]

}
gamehub = json.dumps(gamehub, ensure_ascii=False).encode('utf-8')
gamehub = str(gamehub.decode('utf-8'))

mafiahub = {
    "one_time": False,
    "buttons": [
        [get_button(label="Как играть", color="positive", payload = {'button': 'mafiahub'})],
        [get_button(label="Создать комнату", color="positive", payload = {'button': 'mafiaroomadd'})],
        [get_button(label="Список комнат", color="positive", payload = {'button': 'mafiaroomlist'})],
        [get_button(label="Подключиться к игре", color="positive", payload = {'button': 'mafiainvite'})],
        [get_button(label="Назад", color="negative", payload = {'button': 'gamehub'})]


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
        [get_button(label="Просмотреть предупреждения", color="default", payload = {'button': 'warnlist'})]


    ]
}
warnList = json.dumps(warnList, ensure_ascii=False).encode('utf-8')
warnList = str(warnList.decode('utf-8'))

warnInfo = {
    "inline": True,
    "buttons": [
        [get_button(label="Что это такое?", color="primary", payload = {'button': 'warnInfo'})]


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
            get_button(label="Подтвердить", color="positive", payload = {'button': 'confirm task'}),
            get_button(label="Удалить", color="positive", payload = {'button': 'delete task'}),
            ],

        [get_button(label="Назад", color="negative")]


    ]
}
AModerationTask = json.dumps(AModerationTask, ensure_ascii=False).encode('utf-8')
AModerationTask = str(AModerationTask.decode('utf-8'))


AdminPanel = {
    "one_time": False,
    "buttons": [
        [get_button(label="Статистика", color="positive", payload = {'button': 'statistic'})],
        [get_button(label="Начать модерацию заданий", color="default", payload = {'button': 'task moderation'})],
        [get_button(label="Начать модерацию заметок", color="default", payload = {'button': 'notes moderation'})],
        [get_button(label="Начать модерацию ников", color="default", payload = {'button': 'nick moderation'})],
        [get_button(label="Перезагрузка", color="default", payload = {'button': 'nick moderation'})],
        [get_button(label="Назад", color="negative")]


    ]
}
AdminPanel = json.dumps(AdminPanel, ensure_ascii=False).encode('utf-8')
AdminPanel = str(AdminPanel.decode('utf-8'))



keyboardTasks = {
    "one_time": False,
    "buttons": [
        [get_button(label="Добавить задание", color="positive", payload = {'button': 'add task'}),
        get_button(label="Добавить объявление", color="positive", payload = {'button': 'add ad'})],
        [get_button(label="На завтра", color="default", payload = {'button': 'task', 'date' : 'tomorrow'})],
        [
            get_button(label="На сегодня", color="primary", payload = {'button': 'task', 'date' : 'today'}),
            get_button(label="На послезавтра", color="primary", payload = {'button': 'task', 'date' : 'after'}),
            
            ],
        [get_button(label="Назад", color="negative")]


    ]
}
keyboardTasks = json.dumps(keyboardTasks, ensure_ascii=False).encode('utf-8')
keyboardTasks = str(keyboardTasks.decode('utf-8'))

keyboardGroupChat = {
    #"one_time": True,
    "buttons": [
        [get_button(label="На завтра", color="positive")],
        [
            get_button(label="На сегодня", color="primary"),
            get_button(label="На послезавтра", color="primary"),
            
            ]
        

    ],
    "inline" : True
    
}
keyboardGroupChat = json.dumps(keyboardGroupChat, ensure_ascii=False).encode('utf-8')
keyboardGroupChat = str(keyboardGroupChat.decode('utf-8'))

storageMain = {
    "one_time": True,
    "buttons": [
        [get_button(label="Что это такое? Как пользоваться?", color="positive", payload = {'button': 'storageinfo'})],
        [get_button(label="Добавить файл", color="default", payload = {'button': 'storageadd'})],
        [get_button(label="Мои файлы", color="default", payload = {'button': 'mystoragelist'})],
        [get_button(label="Поиск по базе", color="default", payload = {'button': 'searchstorage'})],
        [get_button(label="Просмотреть файл", color="default", payload = {'button': 'storagedownload'})],
        [get_button(label="Выход", color="negative")],

    ],


}
storageMain = json.dumps(storageMain, ensure_ascii=False).encode('utf-8')
storageMain = str(storageMain.decode('utf-8'))



keyboardNull = {
    "one_time": True,
    "buttons": [
        
    ]#,
    #"inline" : True
    
}
keyboardNull = json.dumps(keyboardNull, ensure_ascii=False).encode('utf-8')
keyboardNull = str(keyboardNull.decode('utf-8'))





keyboardServices = {
    "one_time": True,
    "buttons": [


        [get_button(label="Программирование", color="primary")],
        [get_button(label="Инженерная графика (пусто)", color="negative")],
        [get_button(label="Высшая математика (пусто)", color="negative")],
        [
            get_button(label="Выход", color="default"),
            get_button(label="Инфо", color="default"),
            ]


    ]
}
keyboardServices = json.dumps(keyboardServices, ensure_ascii=False).encode('utf-8')
keyboardServices = str(keyboardServices.decode('utf-8'))

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



        [{ "action": { "type": "vkpay", "hash": "action=transfer-to-group&group_id=182372147&aid=10" }}],
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
        get_button(label="test buttons", color="negative", payload={}),],
        [get_button(label="test buttons", color="negative", payload={}),
        get_button(label="test buttons", color="negative", payload={}),
        get_button(label="test buttons", color="negative", payload={}),
        get_button(label="test buttons", color="negative", payload={}),
        get_button(label="test buttons", color="negative", payload={}),],
        [get_button(label="test buttons", color="negative", payload={}),
        get_button(label="test buttons", color="negative", payload={}),
        get_button(label="test buttons", color="negative", payload={}),
        get_button(label="test buttons", color="negative", payload={}),
        get_button(label="test buttons", color="negative", payload={}),],
        [get_button(label="test buttons", color="negative", payload={}),
        get_button(label="test buttons", color="negative", payload={}),
        get_button(label="test buttons", color="negative", payload={}),
        get_button(label="test buttons", color="negative", payload={}),
        get_button(label="test buttons", color="negative", payload={}),],
        [get_button(label="test buttons", color="negative", payload={}),
        get_button(label="test buttons", color="negative", payload={}),
        get_button(label="test buttons", color="negative", payload={}),
        get_button(label="test buttons", color="negative", payload={}),
        get_button(label="test buttons", color="negative", payload={}),],
        [get_button(label="test buttons", color="negative", payload={}),
        get_button(label="test buttons", color="negative", payload={}),
        get_button(label="test buttons", color="negative", payload={}),
        get_button(label="test buttons", color="negative", payload={}),
        get_button(label="test buttons", color="negative", payload={}),],
    ]

}
coronavirus = json.dumps(coronavirus, ensure_ascii=False).encode('utf-8')
coronavirus = str(coronavirus.decode('utf-8'))

#######################################Keyboards#####################################################
