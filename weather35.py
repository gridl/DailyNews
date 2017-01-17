import json
import logging
import smtplib

import colorlog
import requests
from email.mime.multipart import MIMEMultipart
from config import key, send, recs, wukey

logger = colorlog.getLogger()
cities = ['Beaverton','Portland']
alertcities = []
posts = []


def check_for_alerts():
    try:
        for city in cities:
            r = requests.get("http://api.wunderground.com/api/{}/alerts/q/OR/{}.json".format(wukey, city))
            data = json.loads(r.text)
            logging.info("Alerter Getting {}\n".format(city))
            print("\n-------------------" + (city.upper()) + "-------------------")
            print(data['alerts'])
            if data['alerts']:
                flag = True
                logger.info("{} has Alerts".format(city))
                alertcities.append(city)
                send_mail()
            else:
                flag = False
                logger.info("{} has no Alerts".format(city))
        #print((flag))
        #print('alertcities '+ alertcities)


    except Exception as e:
        logging.DEBUG(e)






def get_weather():
    for city in alertcities:
        try:
            r = requests.get("http://api.wunderground.com/api/{}/alerts/q/OR/{}.json".format(wukey, city))
            data = json.loads(r.text)
            logging.info("Getting {}\n".format(city))
            print("\n-------------------" + (city.upper()) + "-------------------")
            # print(data['alerts'])
            for item in data['alerts']:
                output = str(city.upper()) + '\n' + str((item['date'] + '\n' + item['message']))
                posts.append(output)
            posts.append('\n')
        except Exception as e:
            print(e)
            continue
    return '\n'.join(posts)
        #.encode('utf-8')


def send_mail():
    server = smtplib.SMTP('smtp.mail.yahoo.com', 587)
    server.ehlo()
    server.starttls()
    server.login(send, key)
    # msg = 'Subject: %s\n\n%s' % (SUBJECT, get_posts())
    logger.info("Mailer Getting weather")
    msg = MIMEMultipart()
    msg['Subject'] = 'Weather Alerter'
    msg = (get_weather())

    server.sendmail(send, recs, msg)
    logger.info("Mailer Sending mail")
    server.quit()


if __name__ == '__main__':
    logger.setLevel(colorlog.colorlog.logging.INFO)
    handler = colorlog.StreamHandler()
    handler.setFormatter(colorlog.ColoredFormatter())
    logger.addHandler(handler)
    #send_mail()
    check_for_alerts()
