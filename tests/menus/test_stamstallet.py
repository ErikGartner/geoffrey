from menus.stamstallet import Stamstallet


def test_fetch_menu():
    menu = Stamstallet()
    data = menu._get_week()
    assert len(data['måndag']) > 0
