from menus.bryggan import Bryggan


def test_fetch_menu():
    menu = Bryggan()
    data = menu._get_week()
    assert len(data['Måndag']) > 0
