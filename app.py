import telepot
from flask import Flask, request
from pymongo import MongoClient

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
from modules.lyrics import *


def text_message(msg_recieved, sender_id, msg):
    print sender_id, msg_recieved
    username = msg['from'].get('username')
    msg_list = msg_recieved.split(' ')
    telegram_url = "http://www.telegram.me/"

    if msg_list[0] == '/start':
        send_msg = start()

    elif msg_list[0] == '/tellMeTotalUsers':
        if msg_list[1] == os.environ['FRIDAY_SECRET']:
            if sender_id != 269145190:
                send_msg = "You are not allowed to access this"
                bot.sendMessage('269145190', 'Some New My Secret! Fuck')
            else:
                send_msg = db.users.count()
                # bot.sendMessage('269145190' , db.users.count())


    elif msg_list[0].lower() == '/wiki':
        send_msg = find_wiki(msg_list)

    elif msg_list[0].lower() == '/joke':
        send_msg = randomJoke()

    elif msg_list[0].lower() == '/flip':
        choices = ['Heads', 'Tails']
        send_msg = random.choice(choices)

    elif msg_list[0].lower() == '/quote':
        send_msg = randomQuote()

    elif msg_list[0].lower() == '/shorten':
        if len(msg_list) != 1:
            longUrl = msg_list[1]
            send_msg = "Shortened Url : " + shortUrl(longUrl)
        else:
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

    elif msg_list[0].lower() in ['/lyric', '/lyrics']:
        if len(msg_list) == 1:
            send_msg = "Songname Not Given"
        else:
            try :
                songs = searchLyrics('+'.join(msg_list[1:]))                
                links = []
                for song in songs:
                    bot.sendMessage(sender_id, song['name'] + ' by ' + song['singer'] )
                    links.append(song['link'])
                
                send_download_keyboard(sender_id, links, 'lyrics')
                send_msg = 'Choose Song To Download Lyrics'

            except Exception as e :
                print str(e)
                send_msg = "Lyrics Not Found. Try Another Song."
            

    elif msg_list[0].lower() in ['/video']:
        if len(msg_list) == 1:
            send_msg = "VideoName Not Given"
        else:
            video_names = find_song('+'.join(msg_list[1:]))
            for name in video_names:
                bot.sendMessage(sender_id, name)

            send_download_keyboard(sender_id, video_names, 'video')
            send_msg = 'Choose Video To Download'


    elif msg_list[0].lower() in ['/ytd']:

        if len(msg_list) != 1:
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
            bot.sendMessage('269145190', "Bug Reported : " + str(msg) + '\n\nby   ' + str(telegram_url + username))

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
        if len(msg_list) > 1:
            text = ' '.join(msg_list[1:])
            send_msg = "Message Sent to BotMaster , He will contact you soon."
            bot.sendMessage("269145190", "New Message From " + str(telegram_url + username) + " \n Meesage :- " + text)
        else:
            send_msg = "Usage : to send message to Bot Master \n/contact MESSAGE "
    elif msg_list[0].lower() in ['/news']:
        response = getNews()
        for i in range(2):
            bot.sendMessage(sender_id, response[i])
        keyboardNews = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='More News', callback_data="newsMore")]
        ])
        bot.sendMessage(sender_id, 'Load More', reply_markup=keyboardNews)
        send_msg = "Press Above To Load More News"

    else:
        if "thanks" in msg_list or "Thanks" in msg_list:
            send_msg = "Welcome ,  Show Your Support By Rating Our Bot \n Type /rate to know more"
        else:
            send_msg = "Unknown Command"

    bot.sendMessage(sender_id, send_msg)

    check_user(username, sender_id)


def check_user(username, id):
    telegram_url = "http://www.telegram.me/"
    result = db.users.find_one({'sender_id': id})
    count = None
    print result
    if result:
        count = result['count']
        db.users.update_one({'sender_id': id},
                            {
                                "$set": {
                                    "count": result['count'] + 1
                                }
                            })
    else:
        count = 1
        db.users.insert({'username': username, 'count': 1, 'sender_id': id})
        bot.sendMessage("269145190", "New User Operated")
        bot.sendMessage('269145190', telegram_url + username)


def send_download_keyboard(sender_id, links, type_of_link='song'):
    
    # Inline Keyboard QueryData Can't be reater than 64 Bytes 
 
    mapping = {
        0 : '1st' , 1 : '2nd'  , 2 : '3rd' , 3 : '4th' , 4 : '5th'
    }

    inline_keyboard = [] 

    for i in range(len(links)) : 
        url = links[i]
        if type_of_link == 'lyrics' : 
            url = '/'.join(url.split('/')[-2:])
        button = InlineKeyboardButton(text='Donwload '+ mapping[i] +' Option', callback_data=str(url) + " " + type_of_link)
        inline_keyboard.append([button])
        
    keyboard = InlineKeyboardMarkup( inline_keyboard = inline_keyboard)
    bot.sendMessage(sender_id, 'Use inline keyboard', reply_markup=keyboard)


def download_send_audio(sender_id, song_link):
    song_name = download_song(song_link)
    song = open(song_name, 'rb')
    bot.sendAudio(sender_id, song)
    song.close()

def download_send_lyrics(sender_id, link):
    link = "http://www.azlyrics.com/lyrics/" + link
    lyrics = getLyrics(link)
    bot.sendMessage(sender_id , lyrics)

def download_send_video(sender_id, video_link):
    print video_link
    video_name = download_video(video_link)
    video = open(video_name, 'rb')
    bot.sendVideo(sender_id, video)
    video.close()


def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    print('Callback Query:', query_id, from_id, query_data)
    if query_data == "newsMore":
        bot.answerCallbackQuery(query_id, text='Loading More News')
        response = getNews()
        for i in range(1):
            number = random.randint(2, len(response))
            bot.sendMessage(from_id, response[number])
        
        keyboardNews = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='More News', callback_data="newsMore")]
        ])
        bot.sendMessage(from_id, 'Load More', reply_markup=keyboardNews)

    else:
        type_of_link = query_data.split(' ')[-1]
        link = query_data.split(' ')[0]

        mapping = {
            'song' : download_send_audio,
            'video' : download_send_video, 
            'lyrics' : download_send_lyrics
        }

        bot.sendMessage(from_id, 'Got Your Request! \n Sending...')
        mapping[type_of_link](from_id, link)


def handle(msg):
    sender_id = msg['chat']['id']
    msg_recieved = msg['text']
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type == 'text':
        text_message(msg_recieved, sender_id, msg)


TOKEN = os.environ['TOKEN']
PORT = int(sys.argv[2])
URL =  os.environ['URL']
client = MongoClient(os.environ['MLABFRIDAYURL'])
db = client.friday

app = Flask(__name__)
bot = telepot.Bot(TOKEN)
update_queue = Queue()  # channel between `app` and `bot`

bot.message_loop({'chat': handle, 'callback_query': on_callback_query}, source=update_queue)


@app.route('/verify', methods=['GET', 'POST'])
def pass_update():
    try:
        update_queue.put(request.data)  # pass update to bot
        return 'OK'
    except Exception as e:
        print e
        bot.sendMessage('Error Occured', request.data['chat']['id'])


if __name__ == '__main__':
    bot.setWebhook(URL)
    app.run(port=PORT, debug=True)
