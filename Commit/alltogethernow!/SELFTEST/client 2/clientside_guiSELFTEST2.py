""" Client-side Message Window """

import sys
import tkinter as tk

from client_connectionSELFTEST import Client_Connection
from encryptiondecryptionSELFTEST import Encryptor, Decryptor, gen_keys

from socket import error as socket_error

from configparser import ConfigParser
import os.path


class Client(tk.Frame):

    def __init__(self, parent, width=400, height=500):  # init app
        # creating parent
        tk.Frame.__init__(self, parent)
        self.parent = parent
        parent.title("Client-side")

        Client.get_config(self)

        self.connected = False  # connection identifier

        self.w = width
        self.h = height

        Client.toplevel_menu(self)  # creating chat window

        Client.bind_events(self)  # event binding, such as <enter_pressed>

    def bind_events(self):
        self.enter_field.bind('<Return>', lambda event, a=self: Client.enter_pressed(a))

    def combine_funcs(*funcs):  # function for combining functions
        def combined_func(*args, **kwargs):
            for f in funcs:
                f(*args, **kwargs)

        return combined_func

    def toplevel_menu(self):  # creation of the main window and its widgets
        self.parent.resizable(False, False)

        self.menubar = tk.Menu(self.parent)

        # adding menubar options "Connect", "Options", and "Quit"
        self.menubar.add_command(label="Connect", command=lambda: Client.connection_window(self))
        self.menubar.add_command(label="Disconnect", command=lambda: self.cnct.disconnect())
        self.menubar.add_command(label="Options", command=lambda: Client.options(self))
        self.menubar.add_command(label="Quit", command= Client.combine_funcs(self.parent.destroy, Client.quit_prog))

        # default disconnect bar as disabled
        self.menubar.entryconfig(2, state="disabled")

        # main chat window that can't be edited
        self.messages = tk.Text(self.parent)
        self.messages.config(state='disabled')
        self.messages.grid(row=0, column=0)

        # actual scrollbar
        scrollbar = tk.Scrollbar(self.parent, command=self.messages.yview)
        scrollbar.grid(row=0, column=2, sticky="nsew", padx=2, pady=2)
        self.messages['yscrollcommand'] = scrollbar.set

        """
        #stupid joke scroll window and scrollbar
        scrollW = tk.Toplevel(self.parent)
        scrollW.protocol('WM_DELETE_WINDOW', False)
        scrollb = tk.Scrollbar(scrollW, command=self.messages.yview)
        scrollb.grid(sticky="nsew", padx=2, pady=2)
        self.messages['yscrollcommand'] = scrollb.set"""

        # user input field for chat window
        self.input_user = tk.StringVar()  # make variable for text entry box
        self.enter_field = tk.Entry(self.parent, text=self.input_user)
        self.enter_field.grid(row=20, column=0, sticky='W,E,S,N')  # create entry field

        self.parent.config(menu=self.menubar)  # create menubar

    def enter_pressed(self):  # called if enter is pressed
        input_get = self.enter_field.get()  # getting input from enter box

        # checking if the box contained text, and then acting on that
        if len(input_get) > 0:
            Client.update_text(self, input_get)  # adding the text to the chat window
            if self.connected:
                Client_Connection.send_message(self,
                                               input_get)  # sending the message to the other client, through the server

    def update_text(self, text):  # updating chat window
        self.messages.config(state='normal')  # make text box configurable
        self.messages.insert('end', '{}: {}\n'.format(self.user, text))  # insert message
        self.input_user.set('')  # make entry text box blank
        self.messages.see(tk.END)  # put message box at the end
        self.messages.config(state='disabled')  # make text box unconfigurable

    def connection_window(self):  # window to connect to individual
        top = tk.Toplevel(self.parent)
        tk.Label(top, text="IP:").pack()  # place to enter IP address

        e = tk.Entry(top)  # entry box for IP
        e.pack(padx=5)

        tk.Label(top, text="Port:").pack()  # place to enter port

        e2 = tk.Entry(top)  # entry box for port
        e2.insert(0, 1501)  # defaulted at 1501 to make it easy
        e2.pack(padx=5)

        b = tk.Button(top, text="Enter", command=lambda: Client.combine_funcs(Client.establish_connection(self, e.get(), e2.get()),
                                                                              top.destroy()))
        b.pack(pady=5)  # create and pack confirmation button

    def establish_connection(self, ip, port):  # attempting to establish connection with other client
        try:
            connection = Client_Connection(ip, port)  # launching connection object
            self.menubar.entryconfig(2, state="normal")  # make disconnect viable if connection established
        except socket_error:  # if connection fails
            pass

    def get_config(self):  # retrieving config from local files, creating one if it doesn't exist
        config = ConfigParser()
        if os.path.isfile('config.ini'):  # checking file exists
            config.read('config.ini')  # reading file

            self.user = config['CONFIG']['user']
            self.priv_key = config['CONFIG']['private_key']
            self.pub_key = config['CONFIG']['public_key']
        else:
            self.priv_key, self.pub_key = gen_keys()
            config['CONFIG'] = {'user': 'User',
                                'private_key': self.priv_key,
                                'public_key': self.pub_key}

            with open('config.ini', 'w') as configfile:
                config.write(configfile)
            configfile.close()

    def update_cfg(self):  # updating the config after changes have been made
        config = ConfigParser()
        config.read('config.ini')
        config['CONFIG']['user'] = self.user  # username
        config['CONFIG']['private_key'] = self.priv_key  # private key
        config['CONFIG']['public_key'] = self.pub_key  # public key
        with open('config.ini', 'w') as configfile:  # writing to file
            config.write(configfile)
        configfile.close()

    def options(self):  # allow user to set options, such as name
        window = tk.Toplevel(self.parent)

        tk.Label(window, text="User").grid(row=0)

        e1 = tk.Entry(window)
        e1.grid(row=0, column=1)

        def get_entries(self, *args):  # get the entries the user has input
            ent1 = e1.get()

            if len(ent1) > 0:  # making sure something has been input
                self.user = ent1

            Client.update_cfg(self)

            e1.delete(0, 'end')  # deleting options window

            window.destroy()

        tk.Button(window, text="Enter", command=lambda: get_entries(self, window, e1)).grid(row=3, column=0)

    def quit_prog():  # QUITTING
        sys.exit(0)


root = tk.Tk()
gui = Client(root)
root.mainloop()
