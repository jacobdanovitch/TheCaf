from bs4 import BeautifulSoup
import requests

url = "https://carleton.campusdish.com/Commerce/Catalog/Menus.aspx?LocationId=5087"

def scrape_menu():
    menu = {}
    data = BeautifulSoup(requests.get(url).text, "html.parser")

    stations = data.find_all("div", {"class": "menu-details-station"})

    for station in stations:
        name = station.find("h2", {"class": "collapsible-header"}).get_text()
        if name in ["Grill", "Global", "Farmer’s Market"]:
            menu[name] = [i.get_text() for i in station.find_all("a")]

    return menu

def ask_for_menu():
    menu = scrape_menu()
    speech = ''

    for station in menu:
        if len(menu[station])>0:
            speech += 'At the ' + station + ', there is: '

            for i, food in enumerate(menu[station]):
                speech += " " + food + ("." if (i == len(menu[station])-1) else ",")

            speech += '\n'
    print(speech)

ask_for_menu()