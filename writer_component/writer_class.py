import socket
from random import randint
from datetime import datetime
from threading import Thread
import time

class Writer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
    def start(self):    
        #pokusaj konekcije sa load balancerom  
        try:
            self.socket.connect((self.host, self.port))
            print('Uspesna konekcija.\n')
            
            while True:
                print('Izaberite opciju\n'
                      + '1. Automatsko slanje podataka (CTRL-C za prekid)\n' 
                      + '2. Manuelno slanje podataka\n'
                      + '3. Paljenje\Gasenje workera\n'
                      + '4. Prekid konekcije') 
                case = int(input())
                send_data = ''
                
                if case == 1:
                    while True:
                        try:
                            send_data = self.data_auto()

                            if send_data:
                                response = self.send(send_data)
                                if response == 'Nema odgovora':
                                    break
                                print(response)                    
                            else:
                                print('Poruka nije poslata. Pokusajte ponovo.\n')

                            time.sleep(3)                        
                        except KeyboardInterrupt:
                            break

                elif case == 2:
                    send_data = self.data_input()  
                elif case == 3:
                    print('1. Gasenje workera\n'
                          + '2. Paljenje workera\n') 
                    on_off = int(input())
                    if(on_off != 1 or on_off != 2):
                        print('Greska. Pokusajte ponovo.\n')
                        continue
                    elif on_off == 1:
                        send_data = 'off'
                        response = self.send(send_data)
                    else:
                        send_data = 'on'  
                        response = self.send(send_data)                                                                     
                elif case == 4:
                    send_data = 'end' # saljem 'end' load balanceru da bi on znao da necu vise da pricam s njim
                else:
                    print('Unesite broj izmedju 1-4.\n')
                
                #provera da li je uspesno sakupljen podatak za slanje    
                if send_data:
                    response = self.send(send_data)
                    if response == 'Nema odgovora':
                        break
                    
                    print(response)                    
                else:
                    print('Poruka nije poslata. Pokusajte ponovo.\n')
                    
        except socket.error as e:
            print('Greska u komunikaciji sa load balancerom. ' + str(e))
        finally:
            self.socket.close()
            print('Zavrsena konekcija.\n') 
            
    def send(self, data):
        """Metoda za slanje podataka serveru 

        Args:
            data (string): podatak za slanje

        Returns:
            string: odgovor servera
        """
        self.socket.sendall(data.encode())
                                        
        server_response = self.socket.recv(1024)
                    
        if server_response:
            return server_response.decode()
        else:
            return 'Nema odgovora' #ako nema odgovora od servera zatvara se konekcija
            
    def data_auto(self):
        """Automatsko slanje podataka o trenutim vrednostima brojila.

        Returns:
            string: Podatak za slanje u vidu stringa 'vreme - id_brojila : trenutna_vrednost'
        """

        id = randint(0, 100)
        value = randint(0, 10000)
        dt = datetime.now()
        time_stamp = dt.strftime('%X %x')
        
        return time_stamp + ' - ' + str(id) + ' : ' + str(value)


    def data_input(self):
        print("Unesite id brojila: ")
        id = input()
        print("Unesite vrednost: ")
        value = input()
        return self.data_input_format(id, value)

    def data_input_format(self, id, value):
        """Manuelno slanje podataka o trenutnim vrednostiam brojila.

        Returns:            
            string: Podatak za slanje u vidu stringa 'vreme - id_brojila : trenutna_vrednost'
        """
        try:
            id = int(id)
            value = int(value)
            dt = datetime.now()
            time_stamp = dt.strftime('%X %x')
            return time_stamp + ' - ' + str(id) + ' : ' + str(value)
        except ValueError:
            print("Greska! Vrednosti moraju biti ceo broj.")
            return ""
        except:
            print("Greska!")
            return ""