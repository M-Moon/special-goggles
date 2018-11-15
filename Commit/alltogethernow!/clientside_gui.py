""" Client-side Message Window """

import sys
import tkinter as tk
from client_connection import Client_Connection
from socket import error as socket_error

class Client(tk.Frame):

    def __init__(self, parent, width=400, height=500): # init app
        #creating parent
        tk.Frame.__init__(self, parent)
        self.parent = parent
        parent.title("Client-side")
        self.parent.protocol('WM_DELETE_WINDOW', False)

        self.user = "User"
        
        self.connected = False # connection identifier
        self.cnct = Client_Connection(0) # connector
        
        self.w = width
        self.h = height

        Client.toplevel_menu(self) # creating chat window

        Client.bind_events(self) # event binding, such as <enter_pressed>

    def bind_events(self):
        self.enter_field.bind('<Return>', lambda event, a=self:Client.enter_pressed(a))

    def combine_funcs(*funcs):
        def combined_func(*args, **kwargs):
            for f in funcs:
                f(*args, **kwargs)
        return combined_func

    def toplevel_menu(self): # creation of the main window and its widgets
        self.menubar = tk.Menu(self.parent)

        #adding menubar options "Connect", "Options", and "Quit"
        self.menubar.add_command(label="Connect", command=lambda:Client.connection_window(self))
        self.menubar.add_command(label="Disconnect", command=lambda:self.cnct.disconnect())
        self.menubar.add_command(label="Options", command=lambda:Client.options(self))
        self.menubar.add_command(label="Quit", command=Client.combine_funcs(self.parent.destroy,Client.quit_prog))

        #default disconnect bar as disabled
        self.menubar.entryconfig(2,state="disabled")
        
        #main chat window that can't be edited
        self.messages = tk.Text(self.parent)
        self.messages.config(state='disabled')
        self.messages.grid(row=0,column=0)

        #stupid joke scroll window and scrollbar
        scrollW = tk.Toplevel(self.parent)
        scrollW.protocol('WM_DELETE_WINDOW', False)
        scrollb = tk.Scrollbar(scrollW, command=self.messages.yview)
        scrollb.grid(sticky="nsew", padx=2, pady=2)
        self.messages['yscrollcommand'] = scrollb.set

        #user input field for chat window
        self.input_user = tk.StringVar()
        self.enter_field = tk.Entry(self.parent, text=self.input_user)
        self.enter_field.grid(row=20,column=0,sticky='W,E,S,N')

        self.parent.config(menu=self.menubar)

    def enter_pressed(self): # called if enter is pressed
        input_get = self.enter_field.get() # getting input from enter box

        #checking if the box contained text, and then acting on that
        if len(input_get) > 0:
            Client.update_text(self, input_get) # adding the text to the chat window
            if self.connected:
                Client_Connection.send_message(self, input_get) # sending the message to the other client, through the server

    def update_text(self, text): # updating chat window
        self.messages.config(state='normal')
        self.messages.insert('end', '{}: {}\n'.format(self.user, text))
        self.input_user.set('')
        self.messages.see(tk.END)

    def connection_window(self): # window to connect to individual
        top = tk.Toplevel(self.parent)
        tk.Label(top,text="IP:").pack()

        e = tk.Entry(top)
        e.pack(padx=5)

        b = tk.Button(top,text="Enter",command=lambda:Client.combine_funcs(Client.connect_to_server(self,e.get()),
                                                                           top.destroy()))
        b.pack(pady=5)

    def connect_to_server(self,ip):
        try:
            self.cnct.connect(ip)
            self.menubar.entryconfig(2,state="normal")
        except socket_error:
            pass

    def options(self): # allow user to set options, such as name
        window = tk.Toplevel(self.parent)

        tk.Label(window,text="User").grid(row=0)

        e1 = tk.Entry(window)
        e1.grid(row=0,column=1)

        def get_entries(self,*args):
            ent1 = e1.get()

            if len(ent1) > 0:
                self.user = ent1

            e1.delete(0,'end')

            window.destroy()

        tk.Button(window,text="Enter",command=lambda:get_entries(self,window,e1)).grid(row=3,column=0)

    def quit_prog(): # QUITTING
        sys.exit(0)

root = tk.Tk()
gui = Client(root)
root.mainloop()
