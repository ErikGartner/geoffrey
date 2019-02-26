import requests
from bs4 import BeautifulSoup

from menus.menu import Menu


class FinnInn(Menu):
    def __init__(self):
        super().__init__()
        self.url = 'http://www.finninn.se/lunch-meny/'

    def __repr__(self):
        return ":male_zombie: Finn Inn"

    def _get_week(self):
        """
        Fetches the menu data from the given URL, returns a menu dictionary:
        {
            'dayofweek 1': ['dish 1', 'dish 2', ..., 'dish N'],
            'dayofweek 2': [ ... ]
        }
        """
        content = requests.get(self.url)
        soup = BeautifulSoup(content.text, 'html.parser')
        # menu list
        menu_list = soup.find('ul', {'class': 'menu-items'})
        for li in menu_list.find_all('li', recursive=False):
            # get the day of week
            weekday = (
                li.find('div', {'class': 'grid2column'}).text.strip().lower()
            )
            # get the dishes of the day
            dishes = li.find('div', {'class': 'item-description-menu'}).text

            # add the list of dishes to the menu
            self.menu[weekday] = dishes.strip().split('\n')

        return self.menu
