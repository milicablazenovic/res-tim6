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

        while True: 
            try:
                clientsocket, addr = self.socket.accept()      
                print("Konekcija: %s" % str(addr))
                # ...
            except socket.error as e:
                print("Greska: " + str(e))
             
    def receive_data(self):
        # TODO: Prima podatke od Writera i smesta ih u datoteku
        pass

    def get_data(self):
        # TODO: Prikuplja 10 vrednosti iz datoteke
        pass

    def forward_data(self):
        # TODO: Prosledjuje prikupljene vrednosti prvom slobodnom Workeru
        pass