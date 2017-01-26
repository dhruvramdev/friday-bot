import os , requests

news_token = os.environ['NEWSAPI']

url = "https://newsapi.org/v1/articles?source=the-next-web&sortBy=latest&apiKey=" + news_token

def getNews():
    r = requests.get(url)
    answer = []
    response =  r.json()
    for i in response['articles']:
        content = i['title'] + '\n\n' + i['description'] + "\n\nFind Out More On \n" + i['url']
        answer.append(content)

    return answer
