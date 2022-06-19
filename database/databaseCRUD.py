from asyncio import constants
from itertools import count
from multiprocessing.sharedctypes import Value
import string
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
        return connection
    except cx_Oracle.DatabaseError as er:
        print('Postoji greska sa Oracle bazom:', er)
    except TypeError:
        print("Username, password i dsn moraju biti stringovi!")
        
def db_disconnect():
    if connection:
        connection.close()
        print("Zavrsena konekcija.")


def create_table(connection):
    cursor = connection.cursor()
    try:
        query = f"""create table brojilo(
        idbrojila integer not null,
        ime varchar(20) not null,
        prezime varchar(25) not null,
        ulica varchar(25) not null,
        broj integer not null,
        postbroj integer not null,
        grad varchar(20) not null,
        constraint brojilo_PK primary key (idbrojila))"""
        cursor.execute(query)

        query = f"""create table potrosnja(
        idbrojila integer not null references brojilo,
        potrosnja decimal(10,2) not null,
        mesec integer not null)"""
        cursor.execute(query)

        query = """create sequence auto_inc
                start with 1
                increment by 1
                minvalue 1
                maxvalue 10000"""

        cursor.execute(query)

        connection.commit()
        
    except cx_Oracle.DatabaseError as er:
        print("Greska. Pokusavate da kreirate tabelu sa imenom koje vec postoji.")

def readUsers():
    cursor = connection.cursor()
    cursor.execute("select * from brojilo order by idbrojila")
    rows = cursor.fetchall()
    if rows:
        for item in rows:
            print(item)
    else:
        rows = "Tabela je prazna!"
        print(rows)

    return rows

def deleteUser(idZaBrisanje):
    cursor = connection.cursor()
    cursor.execute("select * from brojilo where idbrojila="+str(idZaBrisanje))
    row = cursor.fetchone()
    if row:
        cursor.execute("delete from brojilo where idbrojila="+str(idZaBrisanje))
        connection.commit()
        result ="Uspesno ste obrisali korisnika!"
        print(result)
        return result
    else:
        result = "Greska, ne postoji ovaj Id u bazi!"
        print(result)
        return result

def createUser(brojilo):
    return brojilo.create_brojilo()
    
def updateUser(id, ime, prezime, ulica, broj, postbroj, grad):
    try:
        if((type(id) != int)):
            raise Exception('Id brojila mora da bude broj!')
        
        if(type(broj) != int and type(broj) != str):
            raise Exception('Broj moze biti u formatu "123" ili "42a"')
        
        #if(type(ime) != str or type(prezime) != str or type(ulica) != str or type(grad) != str):
        #   raise Exception('Nazivi moraju biti stringovi.')
        
        result = all(isinstance(item, int) for item in [id, ime, prezime, ulica, broj, postbroj, grad])
        if result:
            raise Exception('Ime, prezime, ulica, grad moraju biti stringovi.')
    
        
    
        cursor = connection.cursor()
        
        
        cursor.execute("select * from brojilo where idbrojila="+str(id))
        row = cursor.fetchone()
        if row:    
            cursor.execute("UPDATE brojilo SET ime ='"
                            + str(ime) + "', prezime ='"
                            + str(prezime) + "', ulica ='"
                            + str(ulica) + "', broj = "
                            + str(broj) + ", postbroj = "
                            + str(postbroj) + ", grad ='"
                            + str(grad) + "' WHERE idbrojila = " 
                            + str(id))
            connection.commit()
            return "Uspesno ste izmenili korisnika"
        else:
            return "Brojilo ne postoji u sistemu"
    except Exception as e:
        print(e)

def find_id(id, conn):
    cursor = conn.cursor()
    count = 0
    cursor.execute("select * from brojilo where idbrojila="+ str(id))
    for item in cursor:
        count +=1 
    return count

def find_month(id, conn):
    cursor = conn.cursor()
    month = 0
    cursor.execute("select * from potrosnja where idbrojila="+ str(id))
    for item in cursor:
        month += 1

    return month

def update_value(id, value, month, conn):
    cursor = conn.cursor()
    query = f"""insert into potrosnja (idbrojila, potrosnja, mesec)
                values ('{str(id)}', '{str(value)}', '{str(month)}')"""
    cursor.execute(query)
    conn.commit()
    print("Uspesno upisana vrednost.")

    