import cx_Oracle
from database.Brojilo import Brojilo

def db_connect(username='', password='', dsn=''):
    """Konekcija sa Oracle bazom.

    Args:
        username (str, optional): PR1362018. Defaults to ''.
        password (str, optional): ftn. Defaults to ''.
        dsn (str, optional): localhost/xe. Defaults to ''.
    """
    try: 
        global connection 
        connection = cx_Oracle.connect(username, password, dsn)
        print("Konektovali ste se na bazu")
    except cx_Oracle.DatabaseError as er:
        print('Postoji greska sa Oracle bazom:', er)
        
def db_disconnect():
    if connection:
        connection.close()
        print("Zavrsena konekcija.")

def readUsers():
    cursor = connection.cursor()
    cursor.execute("select * from brojilo order by idbrojila")

    for item in cursor:
        print(item)

def deleteUser():
    print("Unesite id brojila za brisanje:")
    idZaBrisanje = input()
    if(len(idZaBrisanje)==0):
        print("Morate uneti id")
    else:
        cursor = connection.cursor()
        cursor.execute("delete from brojilo where idbrojila="+str(idZaBrisanje))

    connection.commit()

def createUser():
    brojilo = Brojilo()
    brojilo.createUser()
    
def updateUser():
    id_update = input("Unesite id brojila koji zelite da izmenite: ")
    
    if(len(id_update)==0):
        print("Morate uneti id")
    else:
        global case
        case = 10
        while case != 7:
            print("Izaberite opciju:\n" + 
                "1. Izmenite ime\n" + 
                "2. Izmenite prezime\n" + 
                "3. Izmenite ulicu\n" + 
                "4. Izmenite broj\n" + 
                "5. Izmenite postanski broj\n" + 
                "6. Izmenite grad\n" + 
                "7. IZLAZ\n")
            
            case = int(input())
            #temp promenljiva za izmenu podataka
            global data_update
            
        
            if case == 1:
                data_update = input("Unesite novo ime: \n")
                cursor = connection.cursor()
                cursor.execute("UPDATE brojilo SET ime ='"
                            + data_update + "' WHERE idbrojila = " + str(id_update))
                connection.commit()
            elif case == 2:
                data_update = input("Unesite novo prezime: \n")
                cursor = connection.cursor()
                cursor.execute("UPDATE brojilo SET prezime ='"
                            + data_update + "' WHERE idbrojila = " + id_update)
                connection.commit()
            elif case == 3:
                data_update = input("Unesite novu ulicu: \n")
                cursor = connection.cursor()
                cursor.execute("UPDATE brojilo SET ulica ='"
                            + data_update + "' WHERE idbrojila = " + id_update)
                connection.commit()
            elif case == 4:
                data_update = input("Unesite novi broj:\n")
                cursor = connection.cursor()
                cursor.execute("UPDATE brojilo SET broj = "
                            + data_update + " WHERE idbrojila = " + id_update)
                connection.commit()
            elif case == 5:
                data_update = input("Unesite novi postanski broj:\n")
                cursor = connection.cursor()
                cursor.execute("UPDATE brojilo SET postanski_broj = "
                            + data_update + " WHERE idbrojila = " + id_update)
                connection.commit()
            elif case == 6:
                data_update = input("Unesite novi grad: \n")
                cursor = connection.cursor()
                cursor.execute("UPDATE brojilo SET grad ='"
                            + data_update + "' WHERE idbrojila = " + id_update)
                connection.commit()
            else:
                print("Molim Vas izaberite obcije 1-6.\n")
        
        print("Izasli ste iz menija za izmenu.\n")