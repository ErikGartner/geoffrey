import requests
import collections

from bs4 import BeautifulSoup

from menus.menu import Menu


class Bryggan(Menu):
    def __init__(self):
        super().__init__()
        self.url = 'https://www.bryggancafe.se/veckans-lunch/'
        self.dow = {
            0: 'Måndag',
            1: 'Tisdag',
            2: 'Onsdag',
            3: 'Torsdag',
            4: 'Fredag',
        }
        self.menu = collections.defaultdict(list)

    def __repr__(self):
        return ":boat: Bryggan Kök och Café"

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
        menu_list = soup.find('div', {'class': 'et_pb_promo_description'})
        last_day = None
        for p in menu_list.find_all('p', recursive=False):
            # get data in each p-tag and ignore em and u tags.
            data = p.text.strip()
            if len(data) == 0:
                continue

            # remove trailing :
            if data[-1] == ':':
                data = data[:-1]

            # now determine if this is a day-label or menu.
            if data in self.dow.values():
                # it was a day label, note it down so we know when we see food
                last_day = data
                continue

            # End of menu.
            if data.startswith('OBS'):
                break
            elif last_day is not None:
                self.menu[last_day].append(data.strip())
        return self.menu


if __name__ == '__main__':
    b = Bryggan()
