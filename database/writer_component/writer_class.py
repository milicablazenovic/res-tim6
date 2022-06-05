import socket
import random
from datetime import datetime

class Writer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
    def start(self):    
        #pokusaj konekcije sa load balancerom  
        try:
            self.socket.connect(self.host, self.port)
            print('Uspesna konekcija.\n')
            
            while True:
                print('Izaberite opciju"\n1. Automatsko slanje podataka\n2. Manuelno slanje podataka\n'
                      +'3. Paljenje\Gasenje workera\n4. Prekid konekcije') 
                case = int(input())
                send_data = ''
                
                if case == 1:
                    send_data = self.data_auto()
                elif case == 2:
                    send_data = self.data_input()   
                elif case == 4:
                       break
                else:
                    print('Unesite broj izmedju 1-4.\n')
                
                #provera da li je uspesno sakupljen podatak za slanje    
                if not send_data:
                    self.socket.sendall(send_data.encode())
                                        
                    server_response = self.socket.recv(1024)
                    
                    if server_response:
                        print(server_response.decode())
                       
                    else:
                        break  #ako nema odgovora od servera zatvara se konekcija
                else:
                    print('Poruka nije poslata.\n')
                    
        except socket.error as e:
            print('Greska u komunikaciji sa load balancerom. ' + str(e))
        finally:
            self.socket.close()
            print('Zavrsena konekcija.\n') 
            
    def data_auto(self):
        """Automatsko slanje podataka o trenutim vrednostima brojila.

        Returns:
            string: Podatak za slanje u vidu stringa 'vreme - id_brojila : trenutna_vrednost'
        """
        id = random.randint(0, 100)
        current_value = random.randint(0, 10000)
        dt = datetime.now()
        time_stamp = dt.strftime('%X %x')
        
        return time_stamp + ' - '  + str(id) + ' : ' + str(current_value)
    
    def data_input(self):
        """Manuelno slanje podataka o trenutnim vrednostiam brojila.

        Returns:            
            string: Podatak za slanje u vidu stringa 'vreme - id_brojila : trenutna_vrednost'
        """
        try:
            print("Unesite ID brojila: ")
            id = int(input())
            print("Unesite vrednost: ")
            current_value = int(input())
            dt = datetime.now()
            time_stamp = dt.strftime('%X %x')
            
            return time_stamp + ' - '  + str(id) + ' : ' + str(current_value)
        except ValueError:
            print("Greska. Vrednosti moraju biti ceo broj.")
            return ""
        except:
            print("Greska.")
            return ""
        
        