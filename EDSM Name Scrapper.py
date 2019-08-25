import requests
from bs4 import BeautifulSoup as bs4

raw_html = requests.get("https://www.edsm.net/en/expeditions").content
html = bs4(raw_html, "html.parser")

links = []
for link in html.find_all("a"):
    formated = link.get("href")
    if formated is not None:
        if "/en/expeditions/summary/" in formated:
            if formated not in links:
                links.append(formated)

ongoing = []
for link in links:
    raw_html = requests.get(f"https://www.edsm.net/{link}").content
    html = bs4(raw_html, "html.parser")
    if "This expedition is finished." not in html.get_text():
        ongoing.append(link)

names = []
for link in ongoing:
    link = link.replace("summary", "participants")
    raw_html = requests.get(f"https://www.edsm.net/{link}").content
    html = bs4(raw_html, "html.parser")
    for text in html.find_all("a"):
        formated = text.get("href")
        if formated is not None:
            if "/en/user/profile/" in formated:
                spot = formated.find("cmdr")
                name = formated[spot + 5:]
                name_clean = name.replace("+", " ")
                if name_clean not in names:
                    names.append(name_clean)

print(names)
