from bs4 import BeautifulSoup
import requests

url = "https://kai.ru"
login_url = "https://kai.ru/main?p_p_id=58&p_p_lifecycle=0&p_p_state=maximized&saveLastPath=false"
login_url = "https://kai.ru/main?p_p_id=58&p_p_lifecycle=1&p_p_state=normal&p_p_mode=view&_58_struts_action=%2Flogin%2Flogin"

data = {
    '_58_formDate': '1663678106245',
    '_58_saveLastPath': "false",
    '_58_redirect': '',
    '_58_doActionAfterLogin': "false",
    '_58_login': '',
    '_58_password': '',
}
session = requests.Session()
res = session.get(login_url, data=data)
cookies = dict(res.cookies)
# print(res.text.replace("  ",'').replace("\n\n","\n").replace("\n\n","\n").replace("\n\n","\n").replace("\n\n","\n").replace("\n\n","\n"))
source = BeautifulSoup(res.text, 'lxml')
capthca_tag = source.find(id="_58_captcha")
if capthca_tag:
    print("IMG is ", capthca_tag["src"])
url = source.find(id='_58_fm')
if url:
    url = url['action']
print("ACTION IS ", url)



p = session.get(capthca_tag["src"])
out = open("img.jpg", "wb")
out.write(p.content)
print(p.text)
out.close()

if capthca_tag:
    data = {
        '_58_formDate': '1663678106245',
        '_58_saveLastPath': "false",
        '_58_redirect': '',
        '_58_doActionAfterLogin': "false",
        '_58_login': '',
        '_58_password': '',
        '_58_captchaText': input("Введите капчу: ")
    }
else:
    data = {
        '_58_formDate': '1663678106245',
        '_58_saveLastPath': "false",
        '_58_redirect': '',
        '_58_doActionAfterLogin': "false",
        '_58_login': 'DobryninIS',
        '_58_password': 'a4c13shj'
    }

result = session.post(url, data = data, cookies = cookies)

url = "https://kai.ru/group/guest/common/about-me"
page = session.get(url)
print(page.text)
