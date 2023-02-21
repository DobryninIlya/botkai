import requests
from bs4 import BeautifulSoup
response = requests.post("https://kai.ru/infoClick/-/info/group?id=21567")

# print(response.text)


soup = BeautifulSoup(response.text, 'lxml')

# print(soup.find("ul", attrs={ "id" : "mylist"}))
list_students = soup.find(id = "p_p_id_infoClick_WAR_infoClick10_")
result = ""
for tag in list_students.find_all("td"):
    if len(tag.text) > 6:
        # if "Староста" in tag.text.strip():
        #     print(tag.text.strip().replace("\n", ""))
        #     break
        result += tag.text.strip().replace("\n", "").replace("                                                                Староста", " (староста)") + "\n"
print(result)
