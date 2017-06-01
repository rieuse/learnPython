import socket

ip_port = ('127.0.0.1', 9999)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(ip_port)
s.listen(5)
while True:
    print("server waiting....")
    conn, addr = s.accept()
    client_data = conn.recv(1024)
    print(str(client_data, 'utf8'))
    conn.sendall(bytes("不存在的", "utf8"))
    conn.close()
