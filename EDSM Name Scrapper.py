import aiohttp
from bs4 import BeautifulSoup as Bs4
from urllib.parse import unquote


async def active_name_generator():
    a = True
    i = 1
    links = []
    while a:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://www.edsm.net/en/expeditions/p/{i}") as response:
                async with session.get(f"https://www.edsm.net/en/expeditions/p/{i - 1}") as pre_response:
                    if await response.text() == await pre_response.text() or i == 1:
                        html = Bs4(await response.text(), "html.parser")
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
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://www.edsm.net/{link}") as response:
                raw_html = await response.text()
        html = Bs4(raw_html, "html.parser")
        if "This expedition is finished." not in html.get_text():
            ongoing.append(link)

    names = {}
    for link in ongoing:
        expedition = link[link.find("name") + 5:]
        expedition_clean = unquote(expedition).replace("+", " ")
        link = link.replace("summary", "participants")
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://www.edsm.net/{link}") as response:
                raw_html = await response.text()
        html = Bs4(raw_html, "html.parser")
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

    return names


async def main():
    names = await active_name_generator()
    print(names)
