from select import select
import socket                                         
import time
from _thread import *

class LoadBalancer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
     
    def writer_handler(self, writersocket):
        while True:
            try:
                # primi podatak od writera:
                data = writersocket.recv(1024).decode()

                # ukoliko je taj podatak 'end' -> prekidam konekciju i sa strane load balancera
                if (data == "end"):
                    break

                writersocket.send('Uspesno poslata poruka na server.'.encode())

                # upisi ga u datoteku:
                self.receive_data(data)
            except socket.error as e:
                print('Greska: ' + str(e))
                break
        
        writersocket.close()
        print('Zavrsena konekcija.')

    def accept_connections(self, socket):
        writersocket, addr = self.socket.accept()
        print('Konekcija: ' + str(addr))
        # kreiraj novi thread svaki put kad se konektuje novi writer:
        start_new_thread(self.writer_handler, (writersocket, ))

    def start(self):
        try:
            self.socket.bind((self.host, self.port))  
        except socket.error as e:
            print('Greska: ' + str(e))

        self.socket.listen() 
        print(f'Load Balancer je pokrenut i slusa na portu {self.port}.\n')   

        while True:
            # prihvataj writer konekcije:
            self.accept_connections(self.socket)

    def receive_data(self, data):        
        try:
            buffer = open ('buffer.txt', 'a')
            buffer.write(data + '\n')
            buffer.close()
        except OSError:
            print('Neuspesno otvaranje fajla!')
            exit()

    def get_data(self):
        # TODO: Prikuplja 10 vrednosti iz datoteke
        pass

    def forward_data(self):
        # TODO: Prosledjuje prikupljene vrednosti prvom slobodnom Workeru
        pass