import copy
import json
import pickle
from pkgutil import get_data
from re import I, T
import select
import socket
import sys                                         
import time
import os
from _thread import *

class LoadBalancer:
    def __init__(self, host, port, host2, port2):
        self.host = host
        self.port = port

        self.host2 = host2
        self.port2 = port2

        self.values = {}

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
     
    def start(self):
        try:
            self.socket.bind((self.host, self.port))  
            self.socket2.bind((self.host2, self.port2)) 
        except socket.error as e:
            print('Greska: ' + str(e))

        self.socket.listen() 
        self.socket2.listen() 
        print(f'Load Balancer je pokrenut i slusa na portu {self.port} i {self.port2}.\n')   

        read_list = [self.socket, self.socket2]

        while True:
            readable, writable, errored = select.select(read_list, [], [])

            for s in readable:
                if s is self.socket:
                    self.accept_connections(self.socket, read_list)
                    
                if s is self.socket2:
                    self.accept_connections2(self.socket2, read_list)

    # WORKERS
    def accept_connections2(self, socket2, read_list):
        worker_socket, address2 = self.socket2.accept()
        read_list.append(worker_socket)
        print('Konekcija: ' + str(address2) + ' na port 8082')
        start_new_thread(self.worker_handler, (worker_socket, ))

    def worker_handler(self, worker_socket):        
        while True:
            num_lines = sum(1 for line in open('buffer.txt'))
            if (num_lines) == 10:                
                # prikupi podatke
                line_array = []
                try:
                    f = open("buffer.txt", "r")
                    for line in f:
                        line_array.append(line)
                except Exception as e:
                    print(e)

                dictionary = {}
                self.parse_data(dictionary, line_array) # parisaranje za slanje
                self.forward_data(dictionary, worker_socket) # slanje workeru
                self.delete_data() # brisanje podataka iz .txt

    # WRITERS
    def accept_connections(self, socket, read_list):
        writer_socket, address = self.socket.accept()
        read_list.append(writer_socket)
        print('Konekcija: ' + str(address) + ' na port 8081')

        start_new_thread(self.writer_handler, (writer_socket, ))

    def writer_handler(self, writer_socket):
        while True:
            try:
                # primi podatak od writera:
                data = writer_socket.recv(1024).decode()

                # ukoliko je taj podatak 'end' -> prekidam konekciju i sa strane load balancera
                if (data == 'end'):
                    break
                # ukoliko je izabrano paljenje/gasenje workera load balancer salje writeru listu upaljenih workera
                if(data.lower() == 'off'):
                    try:
                        f = open("worker_list.txt", 'a+')
                        worker_list = f.readlines() #lista upaljenih workera 
                        writer_socket.send(worker_list.encode())
                        #worker_on = writersocket.recv(1024).decode()
                        pass
                    finally:
                        f.close()
                elif(data.lower() == 'on'):
                    #todo
                    pass

                writer_socket.send('Uspesno poslata poruka na server.'.encode())

                # upisi ga u datoteku:                
                self.receive_data(data)
            except socket.error as e:
                print('Greska: ' + str(e))
                break
        
        writer_socket.close()
        print('Zavrsena konekcija.')

    def receive_data(self, data):        
        try:
            buffer = open('buffer.txt', 'a')
            buffer.write(data + '\n')
            buffer.close()
        except OSError:
            print('Neuspesno otvaranje fajla!')
            exit()

        self.get_data()

    def get_data(self):
        # prikuplja 10 vrednosti iz datoteke:
        line_array = []
        try:
            f = open("buffer.txt", "r")

            count = 0
            for line in f:
                if (count < 10):
                    line_array.append(line)
                    count += 1
                else:
                    break

            f.close()
        except IOError:
            print('Greska pri otvaranju fajla!')

    def parse_data(self, dictionary, line_array):
        for line in line_array:               
            line_pieces = line.split(" ")
            
            id = int(line_pieces[3])
            value = int(line_pieces[5])

            dictionary[id] = value

    def forward_data(self, dictionary, worker_socket):
        try:
            pickled_dictionary = pickle.dumps(dictionary)
            worker_socket.sendall(pickled_dictionary)
            print('Poslato Workeru!')
        except Exception as e:
            print('Greska! ' + e)
    
    def delete_data(self):
        fin = open('buffer.txt', 'r')
        data = fin.read().splitlines(True)

        fout = open('buffer.txt', 'w')
        fout.writelines(data[10:])   