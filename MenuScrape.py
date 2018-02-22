from bs4 import BeautifulSoup
import requests

def scrape_menu(requested_stations):
    menu = {}

    url = "https://carleton.campusdish.com/Commerce/Catalog/Menus.aspx?LocationId=5087"
    data = BeautifulSoup(requests.get(url).text, "html.parser")

    stations = data.find_all("div", {"class": "menu-details-station"})

    for station in stations:
        name = station.find("h2", {"class":"collapsible-header"}).get_text()
        if name in requested_stations:
            menu[name] = [i.get_text() for i in station.find_all("a")]
    return menu


def read_menu(requested_stations=["Grill", "Global", "Farmer’s Market"]):
    menu = scrape_menu(requested_stations)
    speech = ''

    for station in menu:
        speech += 'At the ' + station + ', there is: '

        for food in menu[station]:
            speech += food + ', '

        speech += '.\n'
    return speech



print(read_menu())
