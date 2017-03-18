#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 17:18:39 2017

@author: dhruv
"""

import telepot
import sys
import random
import os
from flask import Flask, request

try:
    from Queue import Queue
except ImportError:
    from queue import Queue

from telepot.namedtuple import *

from modules.youtube import *
from modules.wiki import *
from modules.jokes import *
from modules.feedback import *
from modules.greet import *
from modules.url import *
from modules.news import *

def text_message(msg_recieved, sender_id , msg):
    print sender_id, msg_recieved
    msg_list = msg_recieved.split(' ')

    send_msg = "Bot is Under Maintenance ! Try After Some Time. \n Contact Botmaster At http://telegram.me/dhruvramdev"
    bot.sendMessage(sender_id, send_msg)



def handle(msg):
    sender_id = msg['chat']['id']
    msg_recieved = msg['text']
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type == 'text':
        text_message(msg_recieved, sender_id , msg)


TOKEN = os.environ['TOKEN']
PORT = int(sys.argv[2])
URL =  os.environ['URL'] #"https://ded974f2.ngrok.io/verify"

app = Flask(__name__)
bot = telepot.Bot(TOKEN)
update_queue = Queue()  # channel between `app` and `bot`

bot.message_loop({'chat': handle, 'callback_query': on_callback_query}, source=update_queue)


@app.route('/verify', methods=['GET', 'POST'])
def pass_update():
    update_queue.put(request.data)  # pass update to bot
    return 'OK'


if __name__ == '__main__':
    bot.setWebhook(URL)
    app.run(port=PORT , debug=True)
