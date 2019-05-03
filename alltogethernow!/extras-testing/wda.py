import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '127.0.0.1'
port = 1003
client.connect((host, port))
data = client.recv(1024).decode()
print(data)
dt = "Yo"
bytt = dt.encode() # encode (UTF-8)
client.send(bytt)
