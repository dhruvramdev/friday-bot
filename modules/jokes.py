import requests , random
from bs4 import BeautifulSoup as BS


def randomJoke():
    jokeUrl = "http://www.santabanta.com/jokes/"

    res = requests.get(jokeUrl)
    soup = BS(res.text, 'html.parser')
    result = soup.find_all('span', {'class': 'sms_text'})
    return random.choice(result).text


def randomMeme():
    memeUrl = "http://belikebill.azurewebsites.net/billgen-API.php?default=1"
    res = requests.get(memeUrl)
    file = open("meme.jpg" , "wb")
    for i in res.iter_content(1000):
        file.write(i)
    file.close()
    return "OK"
