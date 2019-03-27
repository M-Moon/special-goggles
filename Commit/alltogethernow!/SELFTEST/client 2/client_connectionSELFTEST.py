""" Class for connecting to the server from the client-side """

import socket
import threading

LOOPBACK_TESTING = '127.0.0.1'

class Client_Connection():

    def __init__(self, ip, port):
        self.ownip = socket.gethostbyname(socket.gethostname())  # get own ip

        self.ip = ip
        self.port = port

    def start_threads(self,trgt):
        threading.Thread(target=self.listen).start()
        threading.Thread(target=self.connect).start()

    def stop_threads(self):
        pass

    def connect(self):
        self.s.connect((self.ip, int(self.port)))

    def disconnect(self):
        pass

    def listen(self):
        listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listen_socket.bind((LOOPBACK_TESTING, 5228))
        listen_socket.listen(1)
        
        while True:
            try:
                connection, address = listen_socket.accept()
                
                #client_socket being the socket assigned to receive msgs
                msg = listen_socket.recv(BUFSIZ).decode("utf8")
                
            except OSError:
                break

    def send_message(self, msg): # sending message to server to be relayed
        pass

    def relay_message(self, msg): # relaying message to GUI part, returning msg
        pass
