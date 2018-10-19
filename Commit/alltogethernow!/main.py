""" Final script """

import tkinter as tk
from threading import Thread

from clientside_gui import Client
#from client_connection import Client_Connection

root = tk.Tk()
app = Client(root)
root.mainloop()
