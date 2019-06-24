import requests
from bs4 import BeautifulSoup

from menus.mop import MOP


class Stamstallet(MOP):
    def __init__(self):
        super().__init__()
        self.url = 'https://stamstallet.se/lunch/'

    def __repr__(self):
        return ":evergreen_tree: Stamstället"
