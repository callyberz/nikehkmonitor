from datetime import datetime
from pytz import timezone
import mysql.connector
import requests

# Convert time to EST.
DATE_CONVERT = datetime.now(timezone('Hongkong'))
DATE = DATE_CONVERT.strftime("%m-%d-%Y %H:%M:%S")


# MYSQL pipleline for storing.
class MYSQL_Pipeline(object):
  def __init__(self):
    # Database connection info. (host, user, password, database)
    print("connecting db")
    self.conn = mysql.connector.connect(host='127.0.0.1', user='root', passwd='', db='monitor', charset="utf8", use_unicode=True)
    self.conn.ping(True)
    self.cursor = self.conn.cursor()

  def process_item(self, item, spider):
    try:
        # print(item)
        self.cursor.execute('INSERT INTO nike (name, link, image, date, size, skucode) VALUES (%s, %s, %s, %s, %s, %s)', (item['name'].encode('utf-8'), item['link'].encode('utf-8'), item['img'].encode('utf-8'), DATE, item['size'].encode('utf-8'), item['skucode'].encode('utf-8')))
    except mysql.connector.errors:
        print("gg")
    finally:
        self.conn.commit()
        requests.post('https://discordapp.com/api/webhooks/570248708826857473/SYiXHw9fAiKwhoThdurtAMVfmtJDfGvVtS9XIbqRsyldvCPj7JsqYU8Z57GhhCpSRCrb', data={
            'content': "**" + item['name'] + "**" + "\n" + item['link'] + "\n" + "\n" + "[ATC]: " + item[
                'size'] + "\n" + "------------" + "\n"})
        print("done now")