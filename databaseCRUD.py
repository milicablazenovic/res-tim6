import cx_Oracle
from Brojilo import Brojilo

connection = cx_Oracle.connect("baza_res", "res", "localhost/xe")
def readUsers():
    cursor = connection.cursor()
    cursor.execute("select * from brojilo")

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
