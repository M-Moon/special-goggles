""" Class for connecting to the server from the client-side """

import socket
from threading import Thread

localhst = "127.0.0.1"

class Client_Connection():

    def __init__(self):
        self.ownip = socket.gethostbyname(socket.gethostname())
        self.connector = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.connector.settimeout(10)
        self.listener.settimeout(10)

    def start_threads(self,trgt):
        listen_thread = Thread(target=Client_Connection.listen).start()
        connect_thread = Thread(target=Client_Connection.connect).start()

    def stop_threads(self):
        pass

    def connect(self, ip, port):
        self.connector.connect((ip, int(port)))

    def disconnect(self):
        self.connector.close()
        self.listener.close()

    def receive(self):
        """ WE BE RECEIVIN' """
        while True:
            try:
                #client_socket being the socket assigned to receive msgs
                msg = client_socket.recv(BUFSIZ).decode("utf8")
            except OSError:
                break

    def send_message(self, msg): # sending message to server to be relayed
        pass

    def relay_message(self, msg): # relaying message to GUI part, returning msg
        pass
