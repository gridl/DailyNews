import json
import logging
import smtplib

import colorlog
import requests

from config import key, send, rec, api

logger = colorlog.getLogger()
newssources = ['the-wall-street-journal', 'techcrunch', 'new-york-magazine', 'bloomberg', 'financial-times',
               'reddit-r-all', 'the-times-of-india', 'business-insider']

posts = []


def get_news_test():
    for newssource in newssources:
        r = requests.get("https://newsapi.org/v1/articles?source={}&sortBy=top&apiKey={}".format(newssource,api))
        data = json.loads(r.text)
        logging.info("Getting {}\n".format(newssource))
        print("\n-------------------" + (newssource.upper()) + "-------------------")
        for article in (data['articles']):
            print(article['title'], article['url'])


def get_news():
    for newssource in newssources:
        r = requests.get("https://newsapi.org/v1/articles?source={}&sortBy=top&apiKey={}".format(newssource,api))
        data = json.loads(r.text)
        logging.info("Getting {}\n".format(newssource))
        posts.append(newssource.upper())
        for article in (data['articles']):
            output = str(article['title'] + " " + str(article['url']) + " " + str(article['publishedAt']))
            posts.append(output)
        posts.append('\n')
    return '\n'.join(posts).encode('utf-8')


def send_mail():
    server = smtplib.SMTP('smtp.mail.yahoo.com', 587)
    server.ehlo()
    server.starttls()
    server.login(send, key)
    #msg = 'Subject: %s\n\n%s' % (SUBJECT, get_posts())
    logger.info("Getting news")
    msg = get_news()
    server.sendmail(send, rec, msg)
    logger.info("Sending mail")
    server.quit()


if __name__ == '__main__':
    logger.setLevel(colorlog.colorlog.logging.INFO)
    handler = colorlog.StreamHandler()
    handler.setFormatter(colorlog.ColoredFormatter())
    logger.addHandler(handler)
    send_mail()
    # get_news_test()
