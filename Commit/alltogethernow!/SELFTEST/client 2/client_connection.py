""" Class for connecting to the server from the client-side """

import socket
from threading import Thread

from encryptiondecryption import encrypt_msg, decrypt_msg

from ast import literal_eval

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

        try: # seeing if listen_thread exists (From previous connection)
            if self.listen_thread:
                pass
        except:
            Client_Connection.listen(self) # create listener

        self.connector.connect((ip, int(port))) # connect function

        # sending key
        self.connector.send(str(self.pub_key).encode('UTF-8'))

        # sending name
        self.connector.send(self.name.encode('UTF-8'))

        print("Connection established") # confirm connection established

    def disconnect(self): # disconnecting by closing both connector and listener sockets
        self.connector.close() # close connector socket
        
        self.listener.close() # close listener socket
        self.connection.close() # close other client connected socket
        #print("Deleted??")

    def listen(self): # starting the listening thread
        self.listen_thread = Thread(target=Client_Connection._listen, args=(self,)).start()

    def _listen(self):
        self.listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # creating listener
        self.listener.settimeout(10) # listener timeout to 10 seconds

        #listener.bind((self.ownip, 4030)) # bind to own ip and arbitrary port
        self.listener.bind(('127.0.0.1', 4030))
        self.listener.listen(1) # listen for one connection, reject all others if connected

        while True:
            self.connection, address = self.listener.accept() # accept incoming connection

            # receiving key
            self.other_pub_key = literal_eval(self.connection.recv(1024).decode())
            #print(self.other_pub_key)

            #receiving name
            self.other_name = self.connection.recv(1024).decode()
            #print(self.other_name)
            
            while True:
                try:
                    data = literal_eval(self.connection.recv(1024).decode()) # receive data and decode, then eval the string to list
                    #print(data)
                    if not data:
                        continue
                    self.incoming_msg = decrypt_msg(self.priv_key, data) # decrypting incoming message
                    #print(self.incoming_msg)  
                except Exception as e:
                    #print(e, "Yes this one right here officer")
                    pass

    def send_message(self, msg): # sending message to other client
        encrypted_msg = encrypt_msg(self.other_pub_key, msg) # encrypt msg with received public key
        self.connector.send(str(encrypted_msg).encode('UTF-8')) # send encrypted msg as string (Cannot send lists easily)

    #def relay_message(self, msg): # relaying message to GUI part, returning msg
      #self.window.update_text(self.other_name, msg)
