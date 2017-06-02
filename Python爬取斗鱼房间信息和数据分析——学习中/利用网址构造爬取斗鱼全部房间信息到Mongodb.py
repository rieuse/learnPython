import re
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

HOST = "http://www.douyu.com"
Directory_url = "http://www.douyu.com/directory?isAjax=1"
Qurystr = "/?page=1&isAjax=1"

client = MongoClient('localhost')
db = client["Douyu2"]
col = db["Roominfo"]


def get_roominfo(data):
    if data:
        firstpage = BeautifulSoup(data, 'lxml')
        roomlist = firstpage.select('li')
        print(len(roomlist))
        if roomlist:
            for room in roomlist:
                try:
                    roomid = room["data-rid"]
                    roomtitle = room.a["title"]
                    roomtitle = roomtitle.encode('utf-8')
                    roomowner = room.select("p > span")
                    roomtag = room.select("div > span")
                    roomimg = room.a
                    roomtag = roomtag[0].string
                    date = datetime.now()
                    if len(roomowner) == 2:
                        zbname = roomowner[0].string
                        audience = roomowner[1].get_text()
                        audience = audience.encode('utf-8').decode('utf-8')
                        image = roomimg.span.img["data-original"]
                        word = u"万"
                        if word in audience:
                            r = re.compile(r'(\d+)(\.?)(\d*)')
                            data = r.match(audience).group(0)
                            audience = int(float(data) * 10000)
                        else:
                            audience = int(audience)
                        roominfo = {
                            "roomid": int(roomid),
                            "roomtitle": roomtitle,
                            "anchor": zbname,
                            "audience": audience,
                            "tag": roomtag,
                            "date": date,
                            "img": image
                        }
                        col.insert_one(roominfo)
                except Exception as e:
                    print(e)


def insert_info():
    session = requests.session()
    pagecontent = session.get(Directory_url).text
    pagesoup = BeautifulSoup(pagecontent, 'lxml')
    games = pagesoup.select('a')
    # col.drop()
    for game in games:
        links = game["href"]
        gameurl = HOST + links + Qurystr
        print(gameurl)
        gamedata = session.get(gameurl).text
        get_roominfo(gamedata)


if __name__ == '__main__':
    insert_info()
