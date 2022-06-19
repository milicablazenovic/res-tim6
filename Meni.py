from threading import BrokenBarrierError
import database.databaseCRUD as databaseCRUD 
from database.Brojilo import Brojilo

global case
case=10       
while case != 5:
    print("Izaberite opciju:\n" + 
        "1. Unesite 1 za kreiranje novog korisnika \n" + 
        "2. Unesite 2 za citanje upisanih korisnika\n" + 
        "3. Unesite 3 za izmenu postojecih korisnika\n" + 
        "4. Unesite 4 za brisanje postojeceg korisnika\n" +
        "5. Unesite 5 za izlaz iz sistema\n")
            
    case = int(input())
    global data_update            
        
    if case == 1:
        print("Unesite ime: ")
        ime = input()
        print("Unesite prezime: ")
        prezime = input()
        print("Unesite ulicu: ")
        ulica = input()
        print("Unesite broj: ")
        broj = input()
        print("Unesite postanski broj: ")
        post_broj = input()
        print("Unesite grad: ")
        grad = input()
        ret_val = databaseCRUD.createUser(Brojilo(ime, prezime, ulica, broj, post_broj, grad))
        print(ret_val)

    elif case == 2:
        databaseCRUD.readUsers()

    elif case == 3:
        print("Unesite id brojila za izmenu:")
        idZaBrisanje = input()
        if(len(idZaBrisanje)==0):
            print("Morate uneti id")
        else:
            print("Unesite novo ime: ")
            ime = input()
            print("Unesite novo prezime: ")
            prezime = input()
            print("Unesite novu ulicu: ")
            ulica = input()
            print("Unesite novi broj: ")
            broj = input()
            print("Unesite novi postanski broj: ")
            post_broj = input()
            print("Unesite novi grad: ")
            grad = input()
            databaseCRUD.updateUser(int(idZaBrisanje), ime, prezime, ulica, broj, post_broj, grad)
        
    elif case == 4:
        print("Unesite id brojila za brisanje:")
        idZaBrisanje = input()
        if(len(idZaBrisanje)==0):
            print("Morate uneti id")
        else:
            databaseCRUD.deleteUser(idZaBrisanje)
    else:
        print("Molim Vas izaberite neke od opcija 1-4.\n")

print("Izasli ste iz menija")



