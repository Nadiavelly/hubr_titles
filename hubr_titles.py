import requests
from bs4 import BeautifulSoup
KEYWORDS = ['дизайн', 'фото', 'web', 'python']

res = requests.get("https://habr.com/ru/all/")
if not res.ok:
    raise Exception("Response is not ok")
text = res.text
soup = BeautifulSoup(text, features="html.parser")
articles = soup.find_all('article')
for article in articles:
    content = []
    hubs = article.find_all('a', class_="tm-article-snippet__hubs-item-link")
    ht = [h.text.strip() for h in hubs]
    content.append(' '.join(ht))
    name = article.find('a', class_="tm-article-snippet__title-link").find('span').text.strip()
    content.append(name)
    words = article.find('div', class_="article-formatted-body article-formatted-body_version-1")
    if words is None:
        words = article.find('div', class_="article-formatted-body article-formatted-body_version-2").find_all('p')
        words = [w.text.strip() for w in words]
        content.append(' '.join(words))
    else:
        content.append(words.text.strip())
    for k in KEYWORDS:
        if k in ' '.join(content):
            href = article.find('h2').find('a', class_='tm-article-snippet__title-link').attrs.get('href')
            date = article.find('span', class_='tm-article-snippet__datetime-published').find('time').attrs.get('title')
            print(f'<{date}>-<{name}>-<https://habr.com{href}>')
            break
