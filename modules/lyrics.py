import requests , random
from bs4 import BeautifulSoup as BS
import urllib 

def searchLyrics(searchString):
    searchUrl = "http://search.azlyrics.com/search.php?q=" + urllib.quote_plus(searchString)

    results = []

    res = requests.get(searchUrl)
    soup = BS(res.text, 'html.parser')
    result = soup.select( 'body > div.container.main-page > div > div > div > table' )
    # print result
    result = result[-1]

    a = result.select('tr')[:-1]
    if len(a) > 5 :
        a = a[1:6]
    for element in a :

        # print element

        name  = element.select('a')[0].text
        link  = element.select('a')[0]['href']
        singer = element.select('b')[1].text

        results.append({
            'name' : name ,
            'link' : link ,
            'singer' : singer
        })
    
    return results

def getLyrics(url) : 

    headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36'}
    res = requests.get(url , headers=headers)
    # print res.text
    soup = BS(res.text, 'html.parser')
    
    result = soup.select('body > div.container.main-page > div > div.col-xs-12.col-lg-8.text-center')

    # print len(result)
    div = result[0].select('div')
    lyrics = div[6].text

    return lyrics

