""" Class for connecting to the server from the client-side """

import socket
from threading import Thread

class Client_Connection():

    def __init__(self, name, pub_key):
        self.ownip = socket.gethostbyname(socket.gethostname()) # getting own ip

        self.pub_key = pub_key # this client's public key
        self.name = name # this client's username

        self.other_pub_key = None # connected client's public key
        self.other_name = None # connected client's name

        self.incoming_msg = None # variable for received messages

    def start_threads(self,trgt): # creating threads so client can both listen and connect
        self.listen_thread = Thread(target=Client_Connection.listen).start()

    def stop_threads(self): # genocide the threads, might not be needed because could just destroy object
        pass

    def connect(self, ip, port): # starting the connection thread
        self.connect_thread = Thread(target=Client_Connection._connect, args=(self, ip, port)).start()

    def _connect(self, ip, port): # connecting to client
        connector = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # creating connector
        connector.settimeout(10) # connector timeout to 10 seconds

        self.connector.connect((ip, int(port)))
        print("Connection established")

        # sending key
        self.connector.send(self.pub_key.encode())

        # receiving key
        self.other_pub_key = self.connector.recv(1024).decode()

        #sending name
        self.connector.send(self.name.encode())

        #receiving name
        self.other_name = self.connector.recv(1024).decode()

    def disconnect(self):
        self.connector.close()
        self.listener.close()

    def listen(self): # starting the listening thread
        self.listen_thread = Thread(target=Client_Connection._listen, args=(self)).start()

    def _listen(self):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # creating listener
        listener.settimeout(10) # listener timeout to 10 seconds

        #listener.bind((self.ownip, 4030)) # bind to own ip and arbitrary port
        listener.bind(('127.0.0.1', 4030))
        listener.listen(1)

        while True:
            connection, address = listener.accept()
            connection.send(self.pub_key.encode())

            while True:
                try:
                    data = connection.recv(1024).decode() # receive data and decode
                    if not data:
                        continue
                    self.incoming_msg = data
                except Exception as e:
                    print(e)

    def send_message(self, msg): # sending message to server to be relayed
        pass

    def relay_message(self, msg): # relaying message to GUI part, returning msg
        pass
