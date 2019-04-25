""" Class for connecting to the server from the client-side """

import socket
from threading import Thread

from encryptiondecryption import encrypt_msg, decrypt_msg

class Client_Connection():

    def __init__(self, name, priv_key, pub_key):
        self.ownip = socket.gethostbyname(socket.gethostname()) # getting own ip

        self.priv_key = priv_key # this client's private key
        self.pub_key = pub_key # this client's public key
        self.name = name # this client's username

        self.other_pub_key = None # connected client's public key
        self.other_name = None # connected client's name

        self.incoming_msg = None # variable for received messages

    def connect(self, ip, port): # connecting to client
        self.connector = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # creating connector
        self.connector.settimeout(10) # connector timeout to 10 seconds

        Client_Connection.listen(self) # create listener

        self.connector.connect((ip, int(port))) # connect function

        # sending key
        self.connector.send(self.pub_key.encode())

        # receiving key
        self.other_pub_key = self.connector.recv(1024).decode()

        #sending name
        self.connector.send(self.name.encode())

        #receiving name
        self.other_name = self.connector.recv(1024).decode()

        print("Connection established") # confirm connection established

    def disconnect(self): # disconnecting by closing both listener and connector objects
        self.connector.close()
        self.listener.close()

    def listen(self): # starting the listening thread
        self.listen_thread = Thread(target=Client_Connection._listen, args=(self,)).start()

    def _listen(self):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # creating listener
        listener.settimeout(10) # listener timeout to 10 seconds

        #listener.bind((self.ownip, 4030)) # bind to own ip and arbitrary port
        listener.bind(('127.0.0.1', 4030))
        listener.listen(1) # listen for one connection

        while True:
            connection, address = listener.accept() # accept incoming connection
            while True:
                try:
                    data = connection.recv(1024).decode() # receive data and decode
                    if not data:
                        continue
                    self.incoming_msg = decrypt_msg(self.priv_key, data)
                    
                    #decrypted_msg = decrypt_msg(self.priv_key, data) # decrypt msg
                    #Client_Connection.relay_message(self, decrypted_msg) # relay to window
                except Exception as e:
                    print(e)

    def send_message(self, msg): # sending message to other client
        encrypted_msg = encrypt_msg(self.other_pub_key, msg) # encrypt msg with received public key
        self.connector.send(encrypted_msg.encode()) # send encrypted msg

    #def relay_message(self, msg): # relaying message to GUI part, returning msg
      #self.window.update_text(self.other_name, msg)
