import requests
import datetime

from menus.menu import Menu


class FinnUt(Menu):
    def __init__(self):
        super().__init__()
        self.url = 'http://finnut.se/ajax/menu.json.php'

    def __repr__(self):
        return ":potato: Finn Ut"

    def _get_week(self):
        """
        Fetches the menu data from the given URL, returns a menu dictionary:
        {
            'dayofweek 1': ['dish 1', 'dish 2', ..., 'dish N'],
            'dayofweek 2': [ ... ]
        }
        """
        content = requests.get(self.url)
        menu_list = content.json()
        for menu in menu_list:
            # date is in the form yyyy-mm-dd
            date = menu['date'].split('-')
            weekday = datetime.date(
                int(date[0]), int(date[1]), int(date[2])
            ).weekday()
            # skip weekends
            if weekday > 4:
                continue
            dow = self.dow[weekday]
            if 'content' not in menu:
                continue
            dishes = menu['content'].split('\n\n')
            # remove the newline for gluten-free etc. and put is between parantheses
            # yes, this is ugly a.f. TODO: make it pretty
            dishes = [
                '%s (%s)' % (i.split('\n')[0], i.split('\n')[1])
                if len(i.split('\n')) > 1
                else i.split('\n')[0]
                for i in dishes
            ]
            self.menu[dow] = dishes

        return self.menu
