import requests
from bs4 import BeautifulSoup

from menus.menu import Menu


class MOP(Menu):
    def __init__(self):
        super().__init__()
        self.url = 'https://morotenopiskan.se/lunch/'

    def __repr__(self):
        return ":carrot: Moroten och Piskan"

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
        menu_list = soup.find(id='content').find('ul')
        for li in menu_list.find_all('li', recursive=False):
            # get the day of week
            weekday = li.find('div', {'class': 'pretty-weekday'}).text.strip()
            menu_items = []
            # get the dishes of the day
            for menu_item in li.find('div', {'class': 'event-info'}).find_all(
                'p'
            ):
                menu_items.append(menu_item.text.strip())

            # add the list of dishes to the menu, but only if it doesn't already
            # exist. Otherwise we'll overwrite the current menu with next week's
            if weekday not in self.menu:
                self.menu[weekday] = menu_items

        return self.menu
