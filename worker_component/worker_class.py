import pickle
from random import randint
import sys
import socket
sys.path.append('../')
from database.databaseCRUD import find_id, find_month, update_value, db_connect
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
                self.recieve_data(self.lb_socket)                          
        except:
            print('Greska u komunikaciji sa load balancerom.')
        finally:
            self.close_socket()
            print('Zavrsena konekcija.\n') 

    def recieve_data(self, socket):
        try:
            data, addr = socket.recvfrom(1024)
            unpickled_list_of_dictionaries = self.load_data(data)
            conn = db_connect("baza_res", "res", "localhost/xe")
            self.save_data(unpickled_list_of_dictionaries, conn)
        except Exception as e:
            print(e)


    def load_data(self, data):
        unpickled_list_of_dictionaries = pickle.loads(data)
        return unpickled_list_of_dictionaries

    def save_data(self, data, conn):
        # podaci koje dolaze su dictionary
        cursor = conn.cursor()

        upisani = []

        for element in data:
            dict_pairs = element.items()
            pairs_iterator = iter(dict_pairs)
            dict = next(pairs_iterator)
            kljuc = dict[0]
            vrednost = dict[1]

            month = 0
            # provera da li prosledjeni id postoji
            count = find_id(kljuc, conn) 
            if count == 0:
                continue # necemo upisati taj podatak
            else:
                # provera koji je sledeci mesec za koji se upisuje vrednost
                month = find_month(kljuc, conn)

                if month == 12:
                    continue
                else:
                    nextMonth = month + 1
                    
                    update_value(kljuc, vrednost, nextMonth, conn)
                    
                    upisani.append({kljuc:vrednost})
        return upisani

    def close_socket(self):
        self.lb_socket.close()


        