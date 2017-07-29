import telepot
import os
import time

TOKEN = os.environ['TOKEN']
bot = telepot.Bot(TOKEN)

from pymongo import MongoClient
client = MongoClient(os.environ['MLABFRIDAYURL'])
db = client.friday


def handle(msg):
    sender_id = msg['chat']['id']
    msg_recieved = msg['text']
    content_type, chat_type, chat_id = telepot.glance(msg)


try:
    bot.message_loop({'chat': handle})
except Exception as error:
    print(error)

msg = """
Now Get the Lyrics of Your Favourite Song By Using the new \n/lyrics command.
Usage :

/lyrics SONGNAME

To show your support to Friday , type /rate and rate us 5 stars.
"""

users = db.users.find({})
for user in users :
    sender_id = user['sender_id']
    # if user['username'] == 'dhruvramdev' : 
        # bot.sendMessage(sender_id , msg)
    
    try :
        bot.sendMessage(sender_id , msg)
        print "Sent to :" , user['username']
    except Exception as e :
        print str(e)
        print "Unable to Send :" , user['username']
        

print "Done"

# Remeber to Delete Webhook before Doing This
