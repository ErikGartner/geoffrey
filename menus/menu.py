class Menu:
    """ Generic super class """

    def __init__(self):
        self.dow = {
            0: 'måndag',
            1: 'tisdag',
            2: 'onsdag',
            3: 'torsdag',
            4: 'fredag',
        }
        self.menu = {}

    def get_week(self):
        try:
            self._get_week()
        except:
            print('Failed to fetch menu for {}'.format(self))
            self.menu = {}

    def _get_week(self):
        raise NotImplementedError

    def get_day(self, dow):
        """
        Returns the menu, as a list, of the given day, dow,
        where 0 is Monday and 6 is Sunday.
        """
        # If the menu hasn't been fetched, do it, it will be cached.
        if self.menu == {}:
            self.get_week()

        dow_name = self.dow[dow]
        if dow_name not in self.menu:
            return ['404 - Food not found']
        return self.menu[dow_name]
