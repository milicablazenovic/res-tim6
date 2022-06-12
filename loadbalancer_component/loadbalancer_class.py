import json
import pickle
from pkgutil import get_data
from re import I, T
from select import select
import socket
import sys                                         
import time
import os
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
                if (data == 'end'):
                    break
                # ukoliko je izabrano paljenje/gasenje workera load balancer salje writeru listu upaljenih workera
                if(data.lower() == 'off'):
                    try:
                        f = open("worker_list.txt", 'r')
                        worker_list = f.readlines() #lista upaljenih workera 
                        writersocket.send(worker_list.encode())
                        #worker_on = writersocket.recv(1024).decode()
                        pass
                    finally:
                        f.close()
                elif(data.lower() == 'on'):
                    #todo
                    pass

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
            buffer = open('buffer.txt', 'a')
            buffer.write(data + '\n')
            buffer.close()
        except OSError:
            print('Neuspesno otvaranje fajla!')
            exit()

        # nakon sto se sacuva nesto u buffer.txt, pozivam funkciju koja ce da radi nad tim podatkom
        self.get_data()

    def parse_data(self, line_array):    
        # npr. 16:44:56 06/07/22 - 29 : 5217           
        dictionary = {}

        for line in line_array:               
            line_pieces = line.split(" ")
            
            id = int(line_pieces[3])
            value = int(line_pieces[5])

            dictionary[id] = value

        # salje ih funkciji koja ce te vrednosti da prosledi prvom slobodnom workeru
        self.forward_data(dictionary)

    
    def get_data(self):
        line_array = []
        try:
            f = open("buffer.txt", "r")

            count = 0
            # prikuplja 10 vrednosti iz datoteke:
            for line in f:
                if (count < 10):
                    line_array.append(line)
                    count += 1
                else:
                    break

            # prikupio 10 vrednosti:
            if (count == 10):
                # salje ih na parsiranje:
                self.parse_data(line_array) 

                # brise ih iz buffer.txt kako bi primio novih 10 vrednosti:
                self.delete_data()

            f.close()
        except IOError:
            print("Greska pri otvaranju fajla!")

    def delete_data(self):
        fin = open('buffer.txt', 'r')
        data = fin.read().splitlines(True)

        fout = open('buffer.txt', 'w')
        fout.writelines(data[10:])

    def forward_data(self, dictionary):
        print("Vrednosti koje ce se slati prvom slobodnom workeru:")
        for key, value in dictionary.items():
            print(key, ' : ', value)

        # salje vrednost workeru (TODO: proveriti koji je slobodan)
        try:
            json_object = json.dumps(dictionary).encode('utf-8')
            self.socket.sendall(json_object)
        except:
            print("Greska!!! Nije provereno koji Worker je slobodan pre slanja (i mozda generalno ne salje dobro)!")