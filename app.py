import telepot
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
    username = msg['from']['username']
    msg_list = msg_recieved.split(' ')
    telegram_url = "http://www.telegram.me/"
    

    if msg_list[0] == '/start':
        send_msg = start()

    elif msg_list[0].lower() == '/wiki':
        send_msg = find_wiki(msg_list)

    elif msg_list[0].lower() == '/joke':
        send_msg = randomJoke()

    elif msg_list[0].lower() == '/flip':
        choices = ['Heads', 'Tails']
        send_msg = random.choice(choices)

    elif msg_list[0].lower() == '/quote' :
        send_msg = randomQuote()

    elif msg_list[0].lower() == '/shorten':
         if len(msg_list) != 1 :
            longUrl = msg_list[1]
            send_msg = "Shortened Url : " + shortUrl(longUrl)
         else :
             send_msg = "URL Not Provided \nUsage : /shorten URL"

    elif msg_list[0].lower() == '/expand':
        if len(msg_list) != 1:
            longUrl = msg_list[1]
            send_msg = "Expaned Url : " + expandUrl(longUrl)
        else:
            send_msg = "URL Not Provided \nUsage : /expand shortURL"


    elif msg_list[0].lower() == '/meme':
        send_msg = randomMeme()
        if send_msg == "OK":
            file = open("meme.jpg", 'rb')
            bot.sendPhoto(sender_id, file)
            file.close()
            send_msg = "Done!"

    elif msg_list[0].lower() in ['/song', '/songs']:
        if len(msg_list) == 1:
            send_msg = "Songname Not Given"
        else:
            song_names = find_song('+'.join(msg_list[1:]))
            for name in song_names:
                bot.sendMessage(sender_id, name)

            send_download_keyboard(sender_id, song_names)
            send_msg = 'Choose Song To Download'

    elif msg_list[0].lower() in ['/ytd']:


        if len(msg_list) != 1 :
            video_name = download_video('+'.join(msg_list[1:]))
            send_msg = 'Done'
            video = open(video_name, 'rb')
            bot.sendMessage(sender_id, 'Uploading')
            bot.sendVideo(sender_id, video)
            video.close()

        else:
            send_msg = "Video Link Not Given \nUsage: /ytd Link"

    elif msg_list[0].lower() in ['/bugs', '/bug']:
        if len(msg_list) != 1:
            text = ' '.join(msg_list[1:])
            send_msg = bug(text)
            bot.sendMessage('269145190', "Bug Reported : " + str(msg ) + '\n\nby   ' + str(telegram_url + username))

        else:
            send_msg = "Usage : /bug Problem"

    elif msg_list[0].lower() in ['/suggest']:
        if len(msg_list) != 1:
            text = ' '.join(msg_list[1:])
            send_msg = suggestion(text)
            bot.sendMessage('269145190', "Suggestion : " + str(msg) + '\n\nby   ' + str(telegram_url + username))

        else:
            send_msg = "Usage : /suggest Suggestion"

    elif msg_list[0].lower() in ['hi', 'hello', 'hey']:
        send_msg = hello()
    elif msg_list[0].lower() in ['help']:
        send_msg = help()

    elif msg_list[0].lower() in ['/rate']:
        send_msg = rate()
    
    elif msg_list[0].lower() in ['/contact']:
        if len(msg_list) > 1 :
            text = ' '.join(msg_list[1:])
            send_msg = "Message Sent to BotMaster , He will contact you soon."
            bot.sendMessage("269145190" , "New Message From " + str(telegram_url + username) + " \n Meesage :- " + text)
        else :
            send_msg = "Usage : to send message to Bot Master \n/contact MESSAGE "
    elif msg_list[0].lower() in ['/news'] :
        response = getNews()
        for i in range(2):
            bot.sendMessage(sender_id , response[i] )
        keyboardNews = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='More News', callback_data="newsMore")]
        ])
        bot.sendMessage(sender_id, 'Load More', reply_markup=keyboardNews)
        send_msg = "Press Above To Load More News"
     
    else:
        if "thanks" in msg_list or "Thanks" in msg_list :
            send_msg = "Welcome ,  Show Your Support By Rating Our Bot \n Type /rate to know more"
        else :
            send_msg = "Unknown Command"

    bot.sendMessage(sender_id, send_msg)
    
    check_user(username)
    
    
def check_user(username) :
    telegram_url = "http://www.telegram.me/"
    file = open("user.txt" , "r")
    users =file.readlines()
    file.close()
    print users
    if username + '\n' not in users :
        bot.sendMessage("269145190" , "New User Operated")
        bot.sendMessage('269145190' , telegram_url + username )
        users.append(username + '\n')
    file = open("user.txt" , "w")
    file.writelines(users)
    file.close()
    

def send_download_keyboard(sender_id, song_names):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Donwload 1st Option', callback_data=song_names[0])],
        [InlineKeyboardButton(text='Donwload 2nd Option', callback_data=song_names[1])],
        [InlineKeyboardButton(text='Donwload 3rd Option', callback_data=song_names[2])],
    ])
    bot.sendMessage(sender_id, 'Use inline keyboard', reply_markup=keyboard)


def download_send_audio(sender_id, song_link):
    song_name = download_song(song_link)
    song = open(song_name, 'rb')
    bot.sendAudio(sender_id, song)
    song.close()


def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    print('Callback Query:', query_id, from_id, query_data)
    if query_data == "newsMore" :
        bot.answerCallbackQuery(query_id, text='Loading More News')
        response = getNews()
        for i in range(1) :
            number = random.randint(2,len(response))
            bot.sendMessage(from_id , response[number] )
        keyboardNews = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='More News', callback_data="newsMore")]
        ])
        bot.sendMessage(from_id, 'Load More', reply_markup=keyboardNews)
    else :
        bot.sendMessage(from_id, 'Got Your Request ! \n Sending File')
        download_send_audio(from_id, query_data)


def handle(msg):
    sender_id = msg['chat']['id']
    msg_recieved = msg['text']
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type == 'text':
        text_message(msg_recieved, sender_id , msg)


TOKEN = os.environ['TOKEN']
PORT = int(sys.argv[2])
URL =  "https://89509e2e.ngrok.io/verify" #os.environ['URL'] 

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
    app.run(debug=True)
