import wikipedia , requests


def find_wiki(msg_list):
    if len(msg_list)== 1 :
        return "Search Query Not Given"
    try :
        return wikipedia.summary(' '.join(msg_list[1:]), sentences=3)
    except wikipedia.exceptions.DisambiguationError :
        return "Please Be More Specific."
    except IndexError:
        return "Incorrect Usage /wiki <query>"
    except:
        return "Failed to Get Query :P"


def randomQuote() :
    url = "http://quotesondesign.com/wp-json/posts?filter[orderby]=rand&filter[posts_per_page]=1"
    r = requests.get(url)
    json = r.json()[0]
    text = json['content'][3:-5] + '\nby ' + json['title']
    return text

randomQuote()
