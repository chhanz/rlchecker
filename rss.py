import os
import sys
import feedparser
import mariadb
import requests
from datetime import datetime

def make_data(baseurl):
    d = feedparser.parse(baseurl)
    for i in d.entries:
        if "Available Now" in i.title:
            cd = datetime.strptime(i.published, '%a, %d %b %Y %X %Z')
            rss_date = str(cd.strftime("%Y-%m-%d"))
            rss_title = i.title
            rss_url = i.link
            cur.execute(f"INSERT IGNORE INTO rss (rss_date, rss_title, rss_url, send) VALUES(\"{rss_date}\",\"{rss_title}\",\"{rss_url}\",\"false\");")
        else:
            pass
    return True

def make_msg():
    msg = ""
    cur.execute("SELECT * FROM rss WHERE send = \"false\"")
    index = cur.fetchall()
    for m in index:
       msg = msg + str(m[0]) + ", " + m[1] + " | <" + m[2] + "|go_page>\n"

    cur.execute("UPDATE rss SET send = 1 WHERE send = 0")
    return msg

def send_msg(data):
    if not data:
        print(str(datetime.now().strftime('[%Y-%m-%d %H:%M:%S]')) + " [INFO] Not Found Release Note")
        return;

    api = os.getenv("SLACK_WEBHOOK")
    slack_channel = os.getenv("SLACK_CHANNEL")
    payload = {
        "channel": slack_channel,
        "attachments": [{
            "color": "#2eb886",
            "pretext": "Rocky Linux Latest Version Checker",
            "title": "Found Rocky Linux Release Note",
            "text": data
        }]
    }
    requests.post(api, json=payload)
    print(str(datetime.now().strftime('[%Y-%m-%d %H:%M:%S]')) + " [INFO] Complete Send Message")
    return True

url = "https://rockylinux.org/rss.xml"

try:
   # DB Connection
   conn = mariadb.connect(user=os.getenv("DB_USER"),
                          password=os.getenv("DB_PASS"),
                          host=os.getenv("DB_HOST"),
                          database=os.getenv("DB_DATABASE"),
                          autocommit=True)
   cur = conn.cursor()

   # Main Application
   make_data(url)
   send_msg(make_msg())

   # Finish DB Connection
   conn.close()
except mariadb.Error as e:
   print(f"Error connecting to MariaDB Platform: {e}")
   sys.exit(1)
