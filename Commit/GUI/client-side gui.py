""" Client-side Message Window """

import sys
import tkinter as tk

class Client(tk.Frame):

    def __init__(self, parent, width, height):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        parent.title("Client-side")

        self.user = "User"
        
        self.w = width
        self.h = height

        Client.toplevel_menu(self)

        Client.bind_events(self)

    def bind_events(self):
        self.enter_field.bind('<Return>', lambda event, a=self:Client.enter_pressed(a))

    def combine_funcs(*funcs):
        def combined_func(*args, **kwargs):
            for f in funcs:
                f(*args, **kwargs)
        return combined_func

    def toplevel_menu(self):
        menubar = tk.Menu(self.parent)
        
        menubar.add_command(label="Connect", command=lambda:Client.connection_window(self))
        menubar.add_command(label="Options", command=lambda:Client.options(self))
        menubar.add_command(label="Quit", command=Client.combine_funcs(self.parent.destroy,Client.quit_prog))

        self.messages = tk.Text(self.parent)
        self.messages.config(state='disabled')
        self.messages.grid(row=0,column=0)

        self.input_user = tk.StringVar()
        self.enter_field = tk.Entry(self.parent, text=self.input_user)
        self.enter_field.grid(row=20,column=0,sticky='W,E,S,N')

        self.parent.config(menu=menubar)

    def enter_pressed(self):
        input_get = self.enter_field.get()
        Client.update_text(self, input_get)

    def update_text(self, text):
        if len(text) > 0:
            self.messages.config(state='normal')
            self.messages.insert('end', '{}: {}\n'.format(self.user, text))
            self.input_user.set('')
            self.messages.see(tk.END)

    def connection_window(self):
        top = tk.Toplevel(self.parent)
        tk.Label(top,text="IP:").pack()

        e = tk.Entry(top)
        e.pack(padx=5)

        b = tk.Button(top,text="Enter",command=lambda:Client.combine_funcs(Client.connect_to_server(self,e.get()),
                                                                           top.destroy()))
        b.pack(pady=5)

    def connect_to_server(self,ip):
        pass

    def options(self):
        window = tk.Toplevel(self.parent)

        tk.Label(window,text="User").grid(row=0)
        tk.Label(window,text="Width").grid(row=1)
        tk.Label(window,text="Height").grid(row=2)

        e1 = tk.Entry(window)
        e2 = tk.Entry(window)
        e3 = tk.Entry(window)
        e1.grid(row=0,column=1)
        e2.grid(row=1,column=1)
        e3.grid(row=2,column=1)

        def get_entries(self,e1,e2,e3):
            ent1 = e1.get()
            ent2 = e2.get()
            ent3 = e3.get()

            if len(ent1) > 0:
                self.user = ent1

            if len(ent2) > 0 or len(ent3) > 0:
                if not ent1.isdigit() and not ent2.isdigit():
                    pass
                elif not ent1.isdigit():
                    self.parent.geometry("400x{}".format(ent2))
                elif not ent2.isdigit():
                    self.parent.geometry("{}x500".format(ent1))
                else:
                    self.parent.geometry("{}x{}".format(ent1,ent2))            

            e1.delete(0,'end')
            e2.delete(0,'end')
            e3.delete(0,'end')

        tk.Button(window,text="Enter",command=lambda:get_entries(self,e1,e2,e3)).grid(row=3,column=0)

    def quit_prog():
        sys.exit(0)

root = tk.Tk()
gui = Client(root, 400, 500)
root.mainloop()
