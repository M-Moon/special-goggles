""" Class for connecting to the server from the client-side """

import socket
from threading import Thread

from encryptiondecryption import encrypt_msg, decrypt_msg

from socket import error as socket_error

from ast import literal_eval

DATA_BUFFER = 16384

class Client_Connection():

    def __init__(self, name, priv_key, pub_key):
        self.priv_key = priv_key # this client's private key
        self.pub_key = pub_key # this client's public key
        self.name = name # this client's username

        self.other_pub_key = None # connected client's public key
        self.other_name = None # connected client's name

        self.incoming_msg = None # variable for received messages

    def get_ownip(self): # script to reliably get own internal ip
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # doesn't even have to be reachable
            s.connect(('10.255.255.255', 1))
            IP = s.getsockname()[0]
        except:
            IP = '127.0.0.1'
        finally:
            s.close()
        return IP

    def connect(self, ip, port): # connecting to client
        self.ip = ip
        self.port = port

        try: # seeing if listen_thread exists (From previous connection)
            if self.listen_thread:
                pass
        except:
            Client_Connection.listen(self) # create listener

        ip_tuple = (self.ip, int(port)) # making ip tuple

        self.connector = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connector.settimeout(10) # connector timeout to 10 seconds

        try:
            self.connector.connect(ip_tuple) # connect function
        except socket_error:
            self.connector.close()
            #print("Closed")

        # sending key
        self.connector.send(str(self.pub_key).encode('UTF-8'))

        # sending name
        self.connector.send(self.name.encode('UTF-8'))

    def disconnect(self): # disconnecting by closing both connector and listener sockets
        self.connector.close() # close connector socket
        
        self.listener.close() # close listener socket
        self.connection.close() # close other client connected socket

        self.other_pub_key = None # getting rid of other client's information
        self.other_name = None

    def listen(self): # starting the listening thread
        self.listen_thread = Thread(target=Client_Connection._listen, args=(self,)).start()

    def _listen(self):
        ownip = Client_Connection.get_ownip(self)
        #print(ownip, "Own")
        
        self.listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # creating listener (ipv4)
        self.listener.settimeout(10) # listener timeout to 10 seconds
        
        if self.ip == '127.0.0.1': # if user trying to connect to themselves, for testing
            self.listener.bind(('127.0.0.1', int(self.port)))
        else:
            self.listener.bind((ownip, int(self.port))) # bind to own ip (ipv4) and same port as connection
        self.listener.listen(1) # listen for one connection, reject all others if connected

        while True:
            try:
                self.connection, address = self.listener.accept() # accept incoming connection

                # receiving key
                self.other_pub_key = literal_eval(self.connection.recv(DATA_BUFFER).decode())

                #receiving name
                self.other_name = self.connection.recv(DATA_BUFFER).decode()
            
                while True:
                    data = literal_eval(self.connection.recv(DATA_BUFFER).decode()) # receive data and decode, then eval the string to list
                    if not data:
                        continue
                    self.incoming_msg = decrypt_msg(self.priv_key, data) # decrypting incoming message 

            except Exception as e:
                #print(e)
                self.listener.close()
                break

    def send_message(self, msg): # sending message to other client
        encrypted_msg = encrypt_msg(self.other_pub_key, msg) # encrypt msg with received public key
        self.connector.send(str(encrypted_msg).encode('UTF-8')) # send encrypted msg as string (Cannot send lists easily)
