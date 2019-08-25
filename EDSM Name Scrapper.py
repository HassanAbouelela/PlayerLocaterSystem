import requests
from bs4 import BeautifulSoup as bs4
from urllib.parse import unquote


a = True
i = 1
links = []
while a:
    raw_html = requests.get(f"https://www.edsm.net/en/expeditions/p/{i}").content
    if raw_html == requests.get(f"https://www.edsm.net/en/expeditions/p/{i-1}").content or i == 1:
        html = bs4(raw_html, "html.parser")
        for link in html.find_all("a"):
            formated = link.get("href")
            if formated is not None:
                if "/en/expeditions/summary/" in formated:
                    if formated not in links:
                        links.append(formated)
        i += 1
    else:
        a = False

ongoing = []
for link in links:
    raw_html = requests.get(f"https://www.edsm.net/{link}").content
    html = bs4(raw_html, "html.parser")
    if "This expedition is finished." not in html.get_text():
        ongoing.append(link)

names = {}
for link in ongoing:
    expedition = link[link.find("name") + 5:]
    expedition_clean = unquote(expedition).replace("+", " ")
    link = link.replace("summary", "participants")
    raw_html = requests.get(f"https://www.edsm.net/{link}").content
    html = bs4(raw_html, "html.parser")
    for text in html.find_all("a"):
        formated = text.get("href")
        if formated is not None:
            if "/en/user/profile/" in formated:
                spot = formated.find("cmdr")
                name = formated[spot + 5:]
                name_clean = unquote(name).replace("+", " ")
                if name_clean not in names:
                    names[name_clean] = []
                names[name_clean].append(expedition_clean)


print(names)
