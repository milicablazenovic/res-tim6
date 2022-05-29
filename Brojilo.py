import cx_Oracle

connection = cx_Oracle.connect("baza_res", "res", "localhost/xe")

class Brojilo:
    ime = ""
    prezime = ""
    ulica = ""
    broj = ""
    postanski_broj = ""
    grad = ""

    def createUser(self):
        if(len(self.ime) == 0):
            print("Unesi ime")
            self.ime = input()
            self.createUser()
            return

        if(len(self.prezime) == 0):
            print("Unesi prezime")
            self.prezime = input()
            self.createUser()
            return

        if(len(self.ulica) == 0):
            print('Unesi ulicu')
            self.ulica = input()
            self.createUser()
            return

        if(len(self.broj) == 0):
            print('Unesi broj')
            self.broj = input()
            self.createUser()
            return

        if(len(self.postanski_broj) == 0):
            print('Unesi postanski broj')
            self.postanski_broj = input()
            self.createUser()
            return
        
        if(len(self.grad) == 0):
            print('Unesi grad')
            self.grad = input()
            self.createUser()
            return

        cursor = connection.cursor()
        cursor.execute("insert into brojilo (ime, prezime, ulica, broj, postanski_broj, grad)" + 
        " values ('" + self.ime + "','" + self.prezime + "','" + self.ulica + "','" + self.broj + "','" + self.postanski_broj + "','" + self.grad + "')")

        connection.commit()