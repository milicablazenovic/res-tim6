import pickle
from pkgutil import get_data
from re import I, T
import select
import socket
from _thread import *
from zoneinfo import available_timezones

# Konstanta za buffer
BUFFER_SIZE = 1024

class LoadBalancer:
    def __init__(self, host, port, host2, port2):
        self.host = host
        self.port = port

        self.host2 = host2
        self.port2 = port2

        #self.values = {}
        
        # inicijalizovan klijentski soket (za writera)
        # self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
     
    def get_workers(self, filename):
        with open(filename) as file:
            lines = file.readlines()
            junk = []
            available_workers = []
            
            if len(lines) == 0:
                print('Konfiguracioni fajl je prazan, izlaz...')
                exit()
                
            for line in lines:
                if line in ['\n', '\r\n']:
                    junk.append(line)
                else:
                    strip_line = line.rstrip() #uklanja whitespaces
                    available_workers.append(strip_line)
                    
        return available_workers
            
    
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
            while True:
                try:
                    num_lines = sum(1 for line in open('buffer.txt'))
                    break
                except Exception as e:
                    pass
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
                list_of_dictionaries = []
                self.parse_data(list_of_dictionaries, line_array) # parisaranje za slanje
                self.forward_data(list_of_dictionaries, worker_socket) # slanje workeru
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
                    worker_list = self.get_workers('workers_list.txt')
                    writer_socket.sendall(worker_list)
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
    
    def parse_data(self, list_of_dictionaries, line_array):
        for line in line_array:    
            line_pieces = line.split(" ")
            
            id = int(line_pieces[3])
            value = int(line_pieces[5])

            list_of_dictionaries.append({id:value})

    def forward_data(self, list_of_dictionaries, worker_socket):
        # postoji zbog testova
        if (type(list_of_dictionaries) is not list):
            return 'Neispravna lista!'
        
        # postoji zbog testova
        if (len(list_of_dictionaries) < 10):
            return 'Nema 10 vrednosti u listi!'

        # postoji zbog testova
        for el in list_of_dictionaries:
            if (type(el) is not dict):
                return 'Neispravni elementi u listi!'

        try:
            pickled_dictionary = pickle.dumps(list_of_dictionaries)
            worker_socket.sendall(pickled_dictionary)
            print('Poslato Workeru!')
            return True
        except Exception as e:
            print('Greska! ' + e)
            return False
    
    def delete_data(self):
        fin = open('buffer.txt', 'r')
        data = fin.read().splitlines(True)

        fout = open('buffer.txt', 'w')
        fout.writelines(data[10:])   

    def close_sockets(self):
        self.socket.close()
        self.socket2.close()