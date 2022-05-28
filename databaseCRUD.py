import cx_Oracle
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
        cursor.execute("delete from brojilo where idbrojila=idZaBrisanje")

    connection.commit()

