""" Class for connecting to the server from the client-side """

import socket
from threading import Thread

class Client_Connection():

    def __init__(self):
        self.ownip = socket.gethostbyname(socket.gethostname()) # getting own ip
    
        self.connector = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # creating connector
        self.listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # creating listener

        self.priv_key = priv_key # this client's private key
        self.pub_key = pub_key # this client's public key

        self.other_priv_key = None # connected client's private key
        self.other_pub_key = None # connected client's public key

        self.connector.settimeout(10) # connector timeout to 10 seconds
        self.listener.settimeout(10) # listener timeout to 10 seconds

    def start_threads(self,trgt): # creating threads so client can both listen and connect
        self.listen_thread = Thread(target=Client_Connection.listen).start()

    def stop_threads(self): # genocide the threads, might not be needed because could just destroy object
        pass

    def connect(self, ip, port): # starting the connection thread
        self.connect_thread = Thread(target=Client_Connection.connect, args=(self, ip, port)).start()

    def _connect(self, ip, port): # connecting to client
        self.connector.connect((ip, int(port)))
        print("Connection established")

    def disconnect(self):
        self.connector.close()
        self.listener.close()

    def listen(self):
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
