import pickle
from random import randint
import sys
import socket
sys.path.append('../')
import database.databaseCRUD as databaseCRUD
import database.months as months


class Worker:
    def __init__(self, lb_host, lb_port):
        self.lb_host = lb_host
        self.lb_port = lb_port 
        self.lb_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        try:
            self.lb_socket.connect((self.lb_host, self.lb_port))
            print('Uspesna konekcija.\n')            
            while True:
                # prihvatamo podatke od LB
                self.recieve_data()                          
        except socket.error as e:
            print('Greska u komunikaciji sa load balancerom. ' + str(e))
        finally:
            self.socket.close()
            print('Zavrsena konekcija.\n') 

    def recieve_data(self):
        try:
            data, addr = self.lb_socket.recvfrom(1024)
            unpickled_dictionary = pickle.loads(data)
            print(unpickled_dictionary)
            self.save_data(unpickled_dictionary)
        except Exception as e:
            print(e)

    def save_data(self, data):
        # podaci koje dolaze su dictionary
        
        databaseCRUD.db_connect("baza_res", "res", "localhost/xe")
        cursor = databaseCRUD.connection.cursor()
        for key in data:
            # key je id a vrednost data[key]
            count = 0
            month = 0
            # provera da li prosledjeni id postoji
            cursor.execute("select * from brojilo where idbrojila="+ str(key))
            for item in cursor:
                count +=1 
            if count == 0:
                continue # necemo upisati taj podatak
            else:
                # provera koji je sledeci mesec za koji se upisuje vrednost
                cursor.execute("select * from potrosnja where idbrojila="+ str(key))
                for item in cursor:
                    month += 1

                if month == 12:
                    continue
                else:
                    nextMonth = month + 1
                    
                    query = f"""insert into potrosnja (idbrojila, potrosnja, mesec)
                            values ('{str(key)}', '{str(data[key])}', '{str(nextMonth)}')"""
                    cursor.execute(query)
                    databaseCRUD.connection.commit()
                    print("Uspesno upisana vrednost.")
            
        