import socket
import time

# 这是一个请求百度的socket示例
# url = 'https://www.baidu.com/'
# host = 'www.baidu.com'
# port = 443
# host_port = (host, port)
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.connect(host_port)
# s.sendall(b'CONNECT url:port/ HTTP/1.1')
# server_replay = s.recv(4096)
# # print(type(server_replay))
# print(str(server_replay, "utf8"))


u = 'type@=loginres/userid@=75788435/roomgroud@=1/pg@=1/sessionid@=3704469000/username@=75788435/nickname@=rieuse/live_stat@=0/is_illegal@=0/ill_ct@=/illts@=0/now@=1496064039/ps@=1/es@=1/it@=0/its@=0/npv@=0/best_dlev@=0/cur_lev@=0/nrc@=0/ih@=0/sahf@=0/'

host = 'openbarrage.douyutv.com'
port = 8601
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
s.send(
    b'GET host:port/type@=loginres/userid@=75788435/roomgroud@=1/pg@=1/sessionid@=3704469000/username@=75788435/nickname@=rieuse/')
server_replay = s.recv(4096)
print(str(server_replay, "utf8"))
