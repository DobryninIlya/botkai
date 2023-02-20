import json
import traceback

from bs4 import BeautifulSoup
import requests
import aiohttp
from ...classes import vk

url = "https://kai.ru"
login_url = "https://kai.ru/main?p_p_id=58&p_p_lifecycle=0&p_p_state=maximized&saveLastPath=false"
login_url = "https://kai.ru/main?p_p_id=58&p_p_lifecycle=1&p_p_state=normal&p_p_mode=view&_58_struts_action=%2Flogin%2Flogin"
parse_scoreboard_url = "https://kai.ru/group/guest/common/about-me?p_p_id=aboutMe_WAR_aboutMe10&p_p_lifecycle=2&p_p_state=normal&p_p_mode=view&p_p_resource_id=getRoleData&p_p_cacheability=cacheLevelPage&p_p_col_id=column-2&p_p_col_count=1"
data = {
    '_58_formDate': '1663678106245',
    '_58_saveLastPath': "false",
    '_58_redirect': '',
    '_58_doActionAfterLogin': "false",
    '_58_login': 'ElizabethII',
    '_58_password': 'Queen',
}

data_captcha = {
    '_58_formDate': '1663678106245',
    '_58_saveLastPath': "false",
    '_58_redirect': '',
    '_58_doActionAfterLogin': "false",
    '_58_login': 'DobryninIS',
    '_58_password': 'a4c13shj',
    '_58_captchaText': ""
}

sessions = []


async def get_autorization_captcha(peer_id):
    global data
    try:
        async with aiohttp.ClientSession() as session:
            async with await session.get(login_url, data=data) as response:
                res = await response.text()
            # cookies = dict(res.cookies)
            source = BeautifulSoup(res, 'lxml')
            capthca_tag = source.find(id="_58_captcha")
            async with await session.get(capthca_tag["src"]) as response:
                p = await response.read()
            out = open("{}.jpg".format(peer_id), "wb")
            out.write(p)
            out.close()
            sessions.append({'user': peer_id,
                             'cookies': session.cookie_jar})
            attachment_id = await get_captcha_attachment(peer_id)
            return attachment_id
    except:
        print('Ошибка:\n', traceback.format_exc())


async def get_captcha_attachment(id):
    a = await vk.docs.getMessagesUploadServer(type="doc", peer_id=id)
    async with aiohttp.ClientSession() as session:
        async with await session.post(a["upload_url"],
                                      data={"file": open(str(id) + ".jpg", "rb")}) as response:
            b = await response.json()

    c = await vk.docs.save(file=b["file"])
    d = "doc" + str(c["doc"]["owner_id"]) + "_" + str(c["doc"]["id"])
    return d


personal_data = {
    'id': None,
    'role_id': None,
    'name': None,
    'lastname': None,
    'fname': None,
    'phone': None,
    'email': None,
    'scorecard_id': None

}

headers = {
    'Accept': 'application/json, text/javascript, */*',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'DNT': '1',
    'Origin': 'https://kai.ru',
    'Referer': 'https://kai.ru/group/guest/common/about-me',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Mobile Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"'
}


async def get_data(id, captcha, login):
    cookie = None
    data_captcha["_58_captchaText"] = captcha
    for session in sessions:
        if session["user"] == id:
            cookie = session['cookies']
    async with aiohttp.ClientSession(cookie_jar=cookie) as session:
        async with await session.post(login_url, data=data_captcha) as response:
            await response.text()
        async with await session.post("https://kai.ru/group/guest/common/about-me") as response:
            res = await response.text()
        source = BeautifulSoup(res, 'lxml')
        surname_tag = source.find(id="_aboutMe_WAR_aboutMe10_lastName")
        if surname_tag['value']:
            personal_data['id'] = id
            personal_data['name'] = source.find(id="_aboutMe_WAR_aboutMe10_firstName")['value']
            personal_data['lastname'] = source.find(id="_aboutMe_WAR_aboutMe10_lastName")['value']
            personal_data['fname'] = source.find(id="_aboutMe_WAR_aboutMe10_middleName")['value']
            personal_data['phone'] = source.find(id="_aboutMe_WAR_aboutMe10_phoneNumber0")['value']
            personal_data['email'] = source.find(id="_aboutMe_WAR_aboutMe10_email")['value']
        try:
            payload = "login={}&tab=student".format(login)
            async with await session.post(parse_scoreboard_url, data=payload, headers=headers) as response:
                res = json.loads(await response.text())["list"]
                actual = res[-1]
                personal_data['scorecard_id'] = actual["zach"]
                personal_data['group_num'] = actual["groupNum"]
                personal_data['group_id'] = actual["groupId"]
                personal_data['full_describe'] = res
                if actual["status"].rstrip() == "Студент":
                    personal_data["role_id"] = 1
                return personal_data
        except:
            print('Ошибка:\n', traceback.format_exc())
