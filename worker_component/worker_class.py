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
        self.lb_socket = socket.socket(socket.AF_INET, socket.SOCK)

    def start(self):
        #pokusaj konekcije sa load balancerom  
        try:
            self.lb_socket.connect((self.lb_host, self.lb_port))
            print('Uspesna konekcija.\n')
            while True:
                #TODO
                #prihvatamo podatke od lb
                self.recieve_data()                          
        except socket.error as e:
            print('Greska u komunikaciji sa load balancerom. ' + str(e))
        finally:
            self.socket.close()
            print('Zavrsena konekcija.\n') 

    def recieve_data(self):
        # TODO: preuzimanje podataka od Load balancera
        response = self.lb_socket.recv(1024).decode()
        self.save_data(response)
        pass

    def save_data(self, data):
        # podaci koje dolaze su oblika id  :  vrednost
        count = 0
        month = 0
        data = data.split(" ")
        id = data[0]
        value = data[::-1][0]
        databaseCRUD.db_connect("baza_res", "res", "localhost/xe")
        cursor = databaseCRUD.connection.cursor()

        # provera da li prosledjeni id postoji
        cursor.execute("select * from brojilo where idbrojila="+ str(id))
        for item in cursor:
            count +=1 
        if count == 0:
            return # necemo upisati taj podatak
        else:
            # provera koji je sledeci mesec za koji se upisuje vrednost
            cursor.execute("select * from potrosnja where idbrojila="+ str(id))
            for item in cursor:
                month += 1

            if month == 12:
                return
            else:
                nextMonth = month + 1
                
                query = f"""insert into potrosnja (idbrojila, potrosnja, mesec)
                        values ('{str(id)}', '{str(value)}', '{str(nextMonth)}')"""
                cursor.execute(query)
                databaseCRUD.connection.commit()
                print("Uspesno upisana vrednost.")
        