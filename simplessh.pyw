"""GUI for shh.py, this should be a proper product of the ssh maanger, complete
   with an easy to use interface. Rewrite of logic in shh.py may be necessary
   to make the program acceptable for use."""

from tkinter import filedialog
from tkinter import *
import subprocess
import threading
import shelve
import sys
import os
import pprint #only used for testing database contents for now

class MainApplication(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        global profile_config, sssh_db

        sssh_db = shelve.open('SSSH_storage.db')

        try:
            profile_config = sssh_db['profile_config']
        except:
            profile_config = {}

        #testing only, currently overide advanced >> button
        def print_dict():
            pprint.pprint(profile_config)
        
        def add_ssh_profile():
            global profile_config, sssh_db
            """add new profile to the connection list database"""
            if add_profile_input.get() != '':
                if add_profile_input.get() not in list(connection_list_window.get(0, END)):
                    connection_list_window.insert(END, add_profile_input.get())
                    name = add_profile_input.get()
                    profile_config[name+'_profile'] = add_profile_input.get()
                    #ssh params
                    profile_config[name+'_server']   = server_input.get()
                    profile_config[name+'_port']     = port_input.get()
                    profile_config[name+'_username'] = username_input.get()
                    profile_config[name+'_password'] = password_input.get()
                    profile_config[name+'_pem']      = pem_input.get()
                    profile_config[name+'_desc']     = description_window.get(1.0, END)
                    #clear boxes
                    add_profile_input.delete(0, END)
                    server_input.delete(0, END)
                    port_input.delete(0, END)
                    username_input.delete(0, END)
                    password_input.delete(0, END)
                    pem_input.delete(0, END)
                    description_window.delete(1.0, END)
                    sssh_db['profile_config'] = profile_config
                    sssh_db.close()
                    sssh_db = shelve.open('SSSH_storage.db')

        def delete_ssh_profile():
            """remove the selected profile and config from the database"""
            global sssh_db
            conn_list = connection_list_window
            name = connection_list_window.selection_get()
            conn_list.delete(connection_list_window.curselection())
            del profile_config[name+'_profile']
            del profile_config[name+'_server']
            del profile_config[name+'_port']
            del profile_config[name+'_username']
            del profile_config[name+'_password']
            del profile_config[name+'_pem']
            del profile_config[name+'_desc']
            sssh_db['profile_config'] = profile_config
            sssh_db.close()
            sssh_db = shelve.open('SSSH_storage.db')

        def save_ssh_config():
            """save changes made to an existing profile"""
            global sssh_db
            #name = connection_list_window \\ will not work until selector is implemented
            name = connection_list_window.selection_get()
            del profile_config[name+'_profile']
            del profile_config[name+'_server']
            del profile_config[name+'_port']
            del profile_config[name+'_username']
            del profile_config[name+'_password']
            del profile_config[name+'_pem']
            del profile_config[name+'_desc']
            profile_config[name+'_profile']  = name
            profile_config[name+'_server']   = server_input.get()
            profile_config[name+'_port']     = port_input.get()
            profile_config[name+'_username'] = username_input.get()
            profile_config[name+'_password'] = password_input.get()
            profile_config[name+'_pem']      = pem_input.get()
            profile_config[name+'_desc']     = description_window.get(1.0, END)
            #clear boxes
            sssh_db['profile_config'] = profile_config
            sssh_db.close()
            sssh_db = shelve.open('SSSH_storage.db')

        def connect_ssh_session():
            """using specified params, connect to the ssh server"""
            name = connection_list_window.selection_get()
            server = server_input.get()
            port = port_input.get()
            username = username_input.get()
            password = password_input.get()
            if pem_input.get() != '':
                pem_key = pem_input.get()
                os.system('xterm -hold -e ssh -i%s %s@%s -p%s' % (pem_key, username, server, port))
            else:
                os.system('xterm -hold -e ssh %s@%s -p%s' % (username, server, port))

        def connect_shell():
            t = threading.Thread(target=connect_ssh_session)
            t.start()

        def dbload():
            """loads the connection profiles from db into client"""
            for profile, v in sssh_db['profile_config'].items():
                if profile.endswith('_profile'):
                    connection_list_window.insert(END, v)

        #more menu functions    
        def onselect(evt):
            """view/load settings on profile select"""
            add_profile_input.delete(0, END)
            server_input.delete(0, END)
            port_input.delete(0, END)
            username_input.delete(0, END)
            password_input.delete(0, END)
            pem_input.delete(0, END)
            description_window.delete(1.0, END)
            name = connection_list_window.selection_get()
            server_input.insert(0, profile_config[name+'_server'])
            port_input.insert(0, profile_config[name+'_port'])
            username_input.insert(0, profile_config[name+'_username'])
            password_input.insert(0, profile_config[name+'_password'])
            pem_input.insert(0, profile_config[name+'_pem'])
            description_window.insert(1.0, profile_config[name+'_desc'])

        def select_pem_key():
            filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("pem files","*.pem"),("all files","*.*")))
            pem_input.insert(END, filename)
        
        #GUI starts here
        #connections list/profiles
        connection_list = Label(text='Profiles')
        connection_list.grid(column=0, row=0)
        connection_list_window = Listbox()
        connection_list_window.grid(column=0, row=1, columnspan=2, sticky=N+S)
        add_profile_input = Entry()
        add_profile_input.grid(column=0, row=2, columnspan=2, sticky=N)
        add_profile = Button(text='Add', command=add_ssh_profile)
        add_profile.grid(column=0, row=3)
        delete_profile = Button(text='Delete', command=delete_ssh_profile)
        delete_profile.grid(column=1, row=3)
        connection_list_window.bind('<<ListboxSelect>>', onselect)

        #profile configure
        profile_setting_title = Label(text='Configure')
        profile_setting_title.grid(column=2, row=0, columnspan=3)
        connection_server = Label(text='Server:')
        connection_server.grid(column=2, row=1, sticky=N+W)
        server_input = Entry()
        server_input.grid(column=2, row=1, sticky=N, pady=20)
        port_number = Label(text='Port:')
        port_number.grid(column=3, row=1, sticky=N+W)
        port_input = Entry()
        port_input.grid(column=3, row=1, sticky=N, pady=20)
        username_tag = Label(text='Username(optional):')
        username_tag.grid(column=2, row=1, sticky=N+W, pady=40)
        username_input = Entry()
        username_input.grid(column=2, row=1, sticky=N, pady=60)
        password_tag = Label(text='Password(optional):')
        password_tag.grid(column=3, row=1, sticky=N+W, pady=40)
        password_input = Entry(show='*')
        password_input.grid(column=3, row=1, sticky=N, pady=60)
        pem_tag = Label(text='.PEM key(optional)')
        pem_tag.grid(column=2, row=1, sticky=N+W, pady=80)
        pem_input = Entry()
        pem_input.grid(column=2, row=1, sticky=N+W, pady=100)
        pick_pem = Button(text='...', command=select_pem_key)
        pick_pem.grid(column=3, row=1, sticky=N+W, pady=92)
        desc_tag = Label(text='Description:')
        desc_tag.grid(column=2, row=1, sticky=S+W, pady=70)
        description_window = Text(width=40, height=5)
        description_window.grid(column=2, row=1, columnspan=3, sticky=S+W, rowspan=2)
        
        #connect/advanced
        connect_to = Button(text='Connect', command=connect_shell)
        connect_to.grid(column=3, row=3, sticky=E)
        advanced_menu = Button(text='Advanced >>', command=print_dict)
        advanced_menu.grid(column=2, row=3, sticky=W)
        save_conn = Button(text='Save', command=save_ssh_config)
        save_conn.grid(column=3, row=3, sticky=W, padx=20)

        root.after(2, dbload)
        
        

if __name__ == "__main__":
    root = Tk()
    root.title('SimpleSSH')
    MainApplication(root).grid()
    root.mainloop()