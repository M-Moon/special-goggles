""" Class for connecting to the server from the client-side """

import socket
from threading import Thread

class Client_Connection():

    def __init__(self, port):
        self.ownip = socket.gethostbyname(socket.gethostname())
        self.s = socket.socket()
        self.port = port

    def start_threads(self,trgt):
        Thread(target=self.receive).start()
        #Thread(target=self.listen).start()

    def stop_threads(self):
        pass

    def connect(self, ip):
        self.s.connect((ip, self.port))

    def disconnect(self):
        self.s.close()

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
