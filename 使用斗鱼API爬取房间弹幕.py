import socket
import time
from pymongo import MongoClient

client = MongoClient('localhost')
db = client["Douyu2"]
col = db["Roominfo"]

HOST = 'http://openbarrage.douyutv.com/'
PORT = 8601
RID = 606118
# LOGIN_INFO = "type@=loginreq/username@=rieuse" + \
#              "/password@=douyu/roomid@=" + str(RID) + "/"
# JION_GROUP = "type@=joingroup/rid@=" + str(RID) + "/gid@=-9999" + "/"
# ROOM_ID = "type@=qrl/rid@=" + str(RID) + "/"
KEEP_ALIVE = "type@=keeplive/tick@=" + \
             str(int(time.time())) + "/vbw@=0/k@=19beba41da8ac2b4c7895a66cab81e23/"


# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def tranMsg(content):
    length = bytearray([len(content) + 9, 0x00, 0x00, 0x00])
    code = length
    magic = bytearray([0xb1, 0x02, 0x00, 0x00])
    end = bytearray([0x00])
    trscont = bytes(content.encode('utf-8'))
    return bytes(length + code + magic + trscont + end)


def create_Conn():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    RID = 606118
    print("当前最热房间:", RID)
    LOGIN_INFO = "type@=loginreq/username@=rieuse" + \
                 "/password@=douyu/roomid@=" + str(RID) + "/"
    print(LOGIN_INFO)
    JION_GROUP = "type@=joingroup/rid@=" + str(RID) + "/gid@=-9999" + "/"
    print(JION_GROUP)
    s.sendall(tranMsg(LOGIN_INFO))
    s.sendall(tranMsg(JION_GROUP))
    return s


def insert_msg(sock):
    sendtime = 0
    while True:
        if sendtime % 20 == 0:
            print("----------Keep Alive---------")
            try:
                sock.sendall(tranMsg(KEEP_ALIVE))
            except socket.error:
                print("alive error")
                sock = create_Conn()
                insert_msg(sock)
        sendtime += 1
        print(sendtime)
        try:
            data = sock.recv(4000)
        except socket.error:
            print("chat error")
            sock = create_Conn()
            insert_msg(sock)
        time.sleep(1)


if __name__ == '__main__':
    insert_msg(create_Conn())
