from flask import Flask
from flask_assistant import Assistant, ask, tell
from bs4 import BeautifulSoup
import requests
import logging

logging.getLogger('flask_assistant').setLevel(logging.DEBUG)

app = Flask(__name__)
assist = Assistant(app, '/')
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

@assist.action("ask-for-menu")
def ask_for_menu():
    menu = scrape_menu()
    speech = ''

    for station in menu:
        if len(menu[station])>0:
            speech += 'At the ' + station + ', there is: '

            for i, food in enumerate(menu[station]):
                speech += " " + food + ("." if (i == len(menu[station])-1) else ",")

            speech += '\n'
    return tell(speech)


if __name__ == '__main__':
    app.run(debug=True)
