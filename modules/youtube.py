from bs4 import BeautifulSoup as BS
import requests
import os
import string


def find_song(query):

    base_url = 'https://www.youtube.com/results?search_query='
    res = requests.get(base_url + query)
    
    soup = BS(res.text, 'html.parser')
    #print soup.prettify() 
    elements = soup.find_all('a', {'class': " yt-uix-sessionlink spf-link "})

    result = []
    for elem in elements :
        result.append('https://www.youtube.com' + elem['href'])
    return result[:3]


def download_song(link):
    link = 'http://www.youtubeinmp3.com/fetch/?format=JSON&video=' + link

    res = requests.get(link)
    download_link = res.json()['link']
    song_name = ''
    for i in res.json()['title']:
        if i in string.ascii_letters + '()-_ ':
            song_name += i



    song_name = os.path.abspath('~')[:-1] + 'songs\\' + song_name  + '.mp3'
    if os.path.isfile(song_name):
        return song_name

    else:
        res = requests.get(download_link)
        file = open(song_name, 'wb')

        for i in res.iter_content(10000):
            file.write(i)

        file.close()
        return song_name


def download_video(yt_link):
    try:
        link = 'http://youtubeinmp4.com/youtube.php?video=' + yt_link

        res = requests.get(link)
        soup = BS(res.text, 'html.parser')
        elem = soup.find('a', {'id': 'downloadMP4'})
        download_link = 'http://youtubeinmp4.com/' + elem['href']
        print(download_link)

        temp = soup.find('h2').text

        video_name = ''
        for i in temp:
            if i in string.ascii_letters + '()-_ ':
                video_name += i

        video_name = os.path.abspath('~')[:-1] + 'videos\\' + video_name + '.mp4'
        res = requests.get(download_link)
        file = open(video_name, 'wb')

        for i in res.iter_content(10000):
            file.write(i)

        file.close()
        return video_name
    except Exception as e:
        print(e , 'exception')
        return None
