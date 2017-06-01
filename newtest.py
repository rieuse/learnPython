# 这个测试用与弹幕的抓取

import multiprocessing
import os
import socket
import sqlite3
import time
from time import localtime

import requests
from bs4 import BeautifulSoup

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = socket.gethostbyname("openbarrage.douyutv.com")
port = 8601
client.connect((host, port))
import re

path = re.compile(b'txt@=(.+?)/cid@')
uid_path = re.compile(b'nn@=(.+?)/txt@')
level_path = re.compile(b'level@=([1-9][0-9]?)/egtt@')


def sendmsg(msgstr):
    msg = msgstr.encode('utf-8')
    data_length = len(msg) + 8
    code = 689
    msgHead = int.to_bytes(data_length, 4, 'little') \
              + int.to_bytes(data_length, 4, 'little') + int.to_bytes(code, 4, 'little')
    client.send(msgHead)
    sent = 0
    while sent < len(msg):
        tn = client.send(msg[sent:])
        sent = sent + tn


def get_name(roomid):
    r = requests.get("http://www.douyu.com/" + roomid)
    soup = BeautifulSoup(r.text, 'lxml')
    return soup.find('a', {'class', 'zb-name'}).string


def keeplive():
    while True:
        msg = 'type@=keeplive/tick@=' + str(int(time.time())) + '/\x00'
        print('init live')
        sendmsg(msg)
        time.sleep(15)


def start(roomid):
    msg = 'type@=loginreq/username@=/password@=/roomid@={}/\x00'.format(roomid)
    sendmsg(msg)
    print(client.recv(1024))
    msg_more = 'type@=joingroup/rid@={}/gid@=-9999/\x00'.format(roomid)
    sendmsg(msg_more)
    if 'danmudata_{}_{}-{}-{}.db'.format(get_name(roomid), localtime().tm_year, localtime().tm_mon,
                                         localtime().tm_mday) in os.listdir('.'):
        print("检测到表已经创建成功!")
        conn = sqlite3.connect(
            'danmudata_{}_{}-{}-{}.db'.format(get_name(roomid), localtime().tm_year, localtime().tm_mon,
                                              localtime().tm_mday))
    else:
        conn = sqlite3.connect(
            'danmudata_{}_{}-{}-{}.db'.format(get_name(roomid), localtime().tm_year, localtime().tm_mon,
                                              localtime().tm_mday))
        conn.execute('''CREATE TABLE DANMU
		    (level INT NOT NULL,
		    NAME CHAR(20) NOT NULL,
		    danmu CHAR(200) NOT NULL
		    );''')
        # f=open('danmudata.txt','a')
    print('连接到{}的直播间'.format(get_name(roomid)))
    while True:
        data = client.recv(1024)
        # print(data)
        data_more = path.findall(data)
        uid_more = uid_path.findall(data)
        level_more = level_path.findall(data)
        if not data:
            break
        else:
            for i in range(0, len(data_more)):
                try:
                    print(
                        "lv:" + level_more[i].decode() + ">>>>>>" + uid_more[i].decode() + ":" + data_more[i].decode())
                    conn.execute(
                        "INSERT INTO DANMU(level,NAME,danmu) VALUES ({0},'{1}','{2}')".format(level_more[i].decode(),
                                                                                              uid_more[i].decode(),
                                                                                              data_more[i].decode()))
                    conn.commit()
                except KeyboardInterrupt:
                    conn.close()
                except:
                    continue


if __name__ == '__main__':
    room_id = input("plz enter the room id")
    p1 = multiprocessing.Process(target=start, args=(room_id,))
    p2 = multiprocessing.Process(target=keeplive)
    p1.start()
    p2.start()
