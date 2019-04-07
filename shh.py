"""logic/cli version for GUI app for managing ssh connections, should be able 
to read list of users, add users, delete users, and make outgoing ssh 
connections. Just another way to manage the default ssh install present in *nix
 and now newer versions of windows."""

import os
import time
import sqlite3

#initiate new users
class SshUsers():
    """users to be added to the sqlite3 database for furture usage,
    includes profile name(nickname), hostname(or ip), and port#"""
    def __init__(self, client_nickname, client_username, client_hostname, client_port):
        self.client_nickname = client_nickname
        self.client_username = client_username
        self.client_hostname = client_hostname
        self.client_port = client_port


#main program funtions after creating client_list.db
def read_users_list():
    """get list of profiles from the db"""
    
    client_detail_list = sqlite3.connect('../db/client_list.db')
    client_db = client_detail_list.cursor()
    
    select = 0
    client_db.execute('SELECT * FROM clients ORDER by ROWID')
    for row in client_db.fetchall():
        clientlist.append(' '.join(row))
    client_detail_list.commit()
    client_detail_list.close()
    for x in clientlist:
        print(str(select)+')', x)
        select += 1
    return clientlist


def create_new_profile():
    """create a new profile(client_nickname) for connections list"""
    client_nickname = input('Enter client profile name: ')
    client_username = input('Enter client username: ')
    client_hostname = input('Enter client hostname: ')
    client_port = '-p' + input('Enter client port: ')
    new_profile = SshUsers(client_nickname, client_username, client_hostname, client_port)
    return add_user_to_db(new_profile)

#recursive from the above function
def add_user_to_db(new_profile):    
        """add profile to the database"""
        try:
            params = (new_profile.client_nickname,
                      new_profile.client_username,
                      new_profile.client_hostname,
                       new_profile.client_port)
            client_db.execute("INSERT INTO clients VALUES (?, ?, ?, ?)", params)
            client_detail_list.commit()
            client_detail_list.close()
        except:
            print('User already exists, try deleting the profile first.')

def remove_user_from_db(choice):
    """remove a user from the database"""
    client_detail_list = sqlite3.connect('../db/client_list.db')
    client_db = client_detail_list.cursor()
    client_db.execute("DELETE FROM clients WHERE nickname=?", (choice,))
    client_detail_list.commit()
    client_detail_list.close()

def connect_session(profile):
    """connect to the selected profile, basic ssh for session now"""
    os.system('ssh ' + profile)

            

if __name__ == '__main__':
    #attach the database
    if not os.path.exists('../db'):
        os.mkdir('../db')
    client_detail_list = sqlite3.connect('../db/client_list.db')
    client_db = client_detail_list.cursor()
    
    try:
        client_db.execute('''CREATE TABLE clients
                            (nickname text, userame text, hostname text, port text)''')
    except:
        pass

    #main menu
    while True:
        #os.system('clear')
        clientlist = []
        print('Here are your current profiles:\n')
        read_users_list()
        print('\nType "create" to make a new profile.')
        choice = input('\nSelect an option: ')
        if choice == 'create':
            os.system('clear')
            create_new_profile()
        else:
            try:
                print('\n' + 'You selected:\n\n' + clientlist[int(choice)])
                confirm = input('\nConnect? (y/n/delete name) to remove: ')
                if confirm == 'y':
                    format_target = clientlist[int(choice)].split(' ')
                    format_target[1]+='@'+format_target[2]
                    format_target.pop(2)
                    ssh_go = ' '.join(format_target[1:])
                    connect_session(ssh_go)
                elif confirm.split(' ')[1]:
                    remove_user_from_db(confirm.split(' ')[1])
            except Exception as e: print(e)

