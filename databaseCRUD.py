import cx_Oracle
connection = cx_Oracle.connect("baza_res", "res", "localhost/xe")
def readUsers():
    cursor = connection.cursor()
    cursor.execute("select * from brojilo")

    for item in cursor:
        print(item)

