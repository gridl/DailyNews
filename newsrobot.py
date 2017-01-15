import requests
import json
import logging
from config import key
import colorlog

logger = colorlog.getLogger()
newssources = ['the-wall-street-journal', 'techcrunch', 'new-york-magazine', 'bloomberg', 'financial-times',
               'reddit-r-all', 'the-times-of-india','business-insider']


def get_news():
    for newssource in newssources:

        r = requests.get(f"https://newsapi.org/v1/articles?source={newssource}&sortBy=top&apiKey={key}")

        data = json.loads(r.text)

        logging.info(f"Getting {newssource}\n")
        print("\n-------------------" + (newssource.upper()) + "-------------------")
        for article in (data['articles']):
            print(article['title'], article['url'])


if __name__ == '__main__':
    logger.setLevel(colorlog.colorlog.logging.INFO)
    handler = colorlog.StreamHandler()
    handler.setFormatter(colorlog.ColoredFormatter())
    logger.addHandler(handler)
    get_news()
