welcome_msg = """
Hey
I am Friday, a Smart Bot on Telegram.

What I can do...
/joke for a random joke
/meme for a random meme
/flip for flipping a coin
/quote for a random Quote
/shorten <url> for shortening a URL
/expand <shortUrl> for expanding a URL
/wiki <keyword> for a searching keyword
/song <songname> for sending song to you
/ytd <link> for downloading youtube video video
/rate for Rating Our Bot

Wanna Report a Bug or send suggestions. Type
/bug <description> to report bug.
/suggest <suggestion> to suggest anything.

"""

hello_msg = """
Hello, This is Friday.
How May I Help You!
"""

rate_msg = """

Rate Frdiay Bot By Clicking Below
http://telegram.me/storebot?start=i_am_friday_bot


"""


def start():
    return welcome_msg

def hello():
    return hello_msg

def help():
    return welcome_msg

def rate():
    return rate_msg
