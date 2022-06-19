import cx_Oracle

#connection = cx_Oracle.connect("PR1362018", "ftn", "localhost/xe")
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
            self.createUser()
            return
        
        if (isinstance(self.postanski_broj, str) == True and len(self.postanski_broj) == 0):
            print('Upisite postanski broj:')
            self.postanski_broj = input()
            self.createUser()
            return

        if(isinstance(self.postanski_broj, str) == True and len(self.postanski_broj) > 0):
            try:
                self.postanski_broj = int(self.postanski_broj)
            except Exception as e:
                print('Neispravan postanski broj, upisite ispravan:')
                self.postanski_broj = input()
                self.createUser()
                return
            self.createUser()
            return

        if(len(self.grad) == 0):
            print('Unesi grad')
            self.grad = input()
            self.createUser()
            return

        self.save_user_to_db()

    def save_user_to_db(self):
        if (self.ime == ''):
            return ('Niste upisali ime!')

        if (self.prezime == ''):
            return ('Niste upisali prezime!')

        if (self.ulica == ''):
            return ('Niste upisali ulicu!')

        if (self.broj == ''):
            return ('Niste upisali broj!')

        if (self.postanski_broj == ''):
            return ('Niste upisali postanski broj!')

        if (isinstance(self.postanski_broj, int) == False):
            return ('Niste upisali validan postanski broj!')

        if (self.grad == ''):
            return ('Niste upisali grad!')
        
        try:
            cursor = connection.cursor()
            cursor.execute("insert into brojilo (ime, prezime, ulica, broj, postbroj, grad)" + 
            " values ('" + self.ime + "','" + self.prezime + "','" + self.ulica + "','" + self.broj + "','" + str(self.postanski_broj) + "','" + self.grad + "')")

            connection.commit()
            return 'Uspesno sacuvan korisnik u bazi!'
        except Exception as e:
            print(e)