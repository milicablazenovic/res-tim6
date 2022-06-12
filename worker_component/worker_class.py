from random import randint
import sys
sys.path.append('../')
import database.databaseCRUD as databaseCRUD
import database.months as months


class Worker:
    def __init__(self):
        pass

    def start(self):
        # TODO: uspostavljanje komunikacije sa Load balancerom
        pass

    def recieve_data(self):
        # TODO: preuzimanje podataka od Load balancera
        pass

    def save_data(self, data):
        # TODO: cuvanje podataka u bazu vodeci racuna da se ne upise u isti red 
        # podaci koje dolaze su oblika id  :  vrednost
        count = 0
        month = 0
        data = data.split(" ")
        id = data[0]
        value = data[::-1][0]
        databaseCRUD.db_connect("baza_res", "res", "localhost/xe")
        cursor = databaseCRUD.connection.cursor()

        # provera da li prosledjeni id postoji
        cursor.execute("select * from brojilo where idbrojila="+ str(id))
        for item in cursor:
            count +=1 
        if count == 0:
            return # necemo upisati taj podatak
        else:
            # provera koji je sledeci mesec za koji se upisuje vrednost
            cursor.execute("select * from potrosnja where idbrojila="+ str(id))
            for item in cursor:
                month += 1

            if month == 12:
                return
            else:
                nextMonth = months.Months(month + 1).name
                
                query = f"""insert into potrosnja (idbrojila, potrosnja, mesec)
                        values ('{str(id)}', '{str(value)}', '{nextMonth}')"""
                cursor.execute(query)
                databaseCRUD.connection.commit()
                print("Uspesno upisana vrednost.")
        