import database.databaseCRUD as databaseCRUD 

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
        databaseCRUD.createUser()

    elif case == 2:
        databaseCRUD.readUsers()

    elif case == 3:
        databaseCRUD.updateUser()
        
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



