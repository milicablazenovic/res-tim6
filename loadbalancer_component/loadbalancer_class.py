from select import select
import socket                                         
import time

class LoadBalancer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
     
    def start(self):
        self.socket.bind((self.host, self.port))          
        self.socket.listen()                                           
        clientsocket, addr = self.socket.accept()      
        print("Konekcija: %s" % str(addr))

        while True: 
            try:
                data = clientsocket.recv(1024).decode()
                clientsocket.send("Uspesno poslata poruka na server.".encode())
                # ...
                self.receive_data(data)

            except socket.error as e:
                print("Greska: " + str(e))
                break 
             
    def receive_data(self, data):
        
        try:
            buffer = open ("buffer.txt", "a")
            buffer.write(data+ '\n')
            buffer.close()
        except OSError:
            print("Neuspesno otvaranje fajla !")
            exit()

    def get_data(self):
        # TODO: Prikuplja 10 vrednosti iz datoteke
        pass

    def forward_data(self):
        # TODO: Prosledjuje prikupljene vrednosti prvom slobodnom Workeru
        pass