#!/usr/bin/env python

import sys
import os
from os import environ as env
import time
import random
import datetime
import json
import importlib

import schedule
from slackclient import SlackClient
from slack_utils import get_user_id, get_channel_id

DEFAULT_MENUS = """[
    "mop.MOP",
    "finninn.FinnInn",
    "bryggan.Bryggan",
    "edison.Edison",
    "inspira.Inspira"
]"""

CONFIG = {
    'BOT_NAME': env.get('BOT_NAME', 'Gordon'),
    'BOT_ID': env.get('BOT_ID', ''),
    'BOT_CHANNEL': env.get('BOT_CHANNEL'),
    'BOT_CHANNEL_ID': env.get('BOT_CHANNEL_ID', ''),
    'API_TOKEN': env.get('API_TOKEN'),
    'MENUS': json.loads(env.get('MENUS', DEFAULT_MENUS)),
    'POST_TIME': env.get('POST_TIME', '8:00'),
    'UPDATE_TIME': env.get('UPDATE_TIME', '11:00'),
}

AT_BOT = ''

# load the menu classes dynamically
menu_classes = []
for menu in CONFIG['MENUS']:
    full_path = 'menus.%s' % menu
    class_data = full_path.split('.')
    mod_path = '.'.join(class_data[:-1])
    class_str = class_data[-1]
    mod = importlib.import_module(mod_path)
    cls = getattr(mod, class_str)
    menu_classes.append(cls)

# set up slack connection
slackc = SlackClient(CONFIG['API_TOKEN'])

# map the day of week numbers to the actual names, in swedish
weekdays = {0: 'måndag', 1: 'tisdag', 2: 'onsdag', 3: 'torsdag', 4: 'fredag'}


def post_lunch(dow, channel):
    """ Posts today's menu from all included restaurants """
    # don't post on weekends
    if dow > 4:
        return

    resp = (
        '*Lunch of the Day (%s):*\n------------------------------------\n\n'
        % weekdays[dow]
    )
    for menu in menu_classes:
        menu_obj = menu()
        # only show Avesta menu on fridays
        # TODO: this should be entered in the CONFIGig file
        if dow != 4 and 'Avesta' in str(menu_obj):
            continue
        dishes = menu_obj.get_day(dow)
        resp += '*%s*\n' % menu_obj
        for dish in dishes:
            resp += '- \t%s\n' % dish

    resp += '\n_Yours Truly_,\n%s' % CONFIG['BOT_NAME']

    slackc.api_call(
        'chat.postMessage', channel=channel, text=resp, as_user=True
    )


def post_today(channel):
    print('Posting menus...')
    today = datetime.datetime.today().weekday()
    post_lunch(today, channel)


def update_lunch():
    """ Update the menu, caching it """
    print('Updating menus...')
    for menu in menu_classes:
        # the function caches the menu
        menu().get_week()


def post_msg(msg, channel):
    slackc.api_call('chat.postMessage', channel=channel, text=msg, as_user=True)


if __name__ == '__main__':
    if CONFIG['BOT_ID'] == '':
        CONFIG['BOT_ID'] = get_user_id(slackc, CONFIG['BOT_NAME'])
        if CONFIG['BOT_ID'] == None:
            print('Error: Could not get the bot ID')
            sys.exit(1)
    if CONFIG['BOT_CHANNEL_ID'] == '':
        CONFIG['BOT_CHANNEL_ID'] = get_channel_id(slackc, CONFIG['BOT_CHANNEL'])
        if CONFIG['BOT_CHANNEL_ID'] == None:
            print('Error: Could not get the bot channel ID')
            sys.exit(1)

    AT_BOT = '<@%s>' % CONFIG['BOT_ID']

    # seconds to sleep between reading
    READ_DELAY = 1

    UPDATE_TIME = CONFIG['UPDATE_TIME']
    schedule.every().day.at(UPDATE_TIME).do(update_lunch)
    update_lunch()

    # set up schedule for posting lunch
    POST_TIME = CONFIG['POST_TIME']
    schedule.every().day.at(POST_TIME).do(post_today, CONFIG['BOT_CHANNEL_ID'])

    if slackc.rtm_connect():
        print('%s is ready to serve!' % CONFIG['BOT_NAME'])
        while True:
            schedule.run_pending()
            time.sleep(READ_DELAY)
