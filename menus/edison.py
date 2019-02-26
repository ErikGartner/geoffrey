import requests
from bs4 import BeautifulSoup

from menus.menu import Menu


class Edison(Menu):
    def __init__(self):
        super().__init__()
        self.url = 'http://restaurangedison.se/lunch'
        self.dow = {
            0: 'monday',
            1: 'tuesday',
            2: 'wednesday',
            3: 'thursday',
            4: 'friday',
        }

    def __repr__(self):
        return ":bulb: Edison"

    def _get_week(self):
        """
        Fetches the menu data from the given URL, returns a menu dictionary:
        {
            'dayofweek 1': ['dish 1', 'dish 2', ..., 'dish N'],
            'dayofweek 2': [ ... ]
        }
        """
        content = requests.get(self.url)
        soup = BeautifulSoup(content.text, 'html5lib')
        # menu list
        for weekday in self.dow.values():
            day_menu = soup.find('div', {'id': weekday})
            dishes = []
            for dish in day_menu.find_all('tr'):
                txt = dish.find('td', {'class': 'course_type'}).text.strip()
                txt += (
                    ': '
                    + dish.find(
                        'td', {'class': 'course_description'}
                    ).text.strip()
                )
                dishes.append(txt)
            self.menu[weekday] = dishes
        return self.menu
