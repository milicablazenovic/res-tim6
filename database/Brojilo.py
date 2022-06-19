import cx_Oracle

connection = cx_Oracle.connect("PR1362018", "ftn", "localhost/xe")
#connection = cx_Oracle.connect("baza_res", "res", "localhost/xe")

class Brojilo:
    ime = ""
    prezime = ""
    ulica = ""
    broj = ""
    postanski_broj = ""
    grad = ""

    def __init__(self, ime, prez, ul, br, po_br, grad):
        self.ime = ime
        self.prezime = prez
        self.ulica  = ul
        self.broj = br
        self.postanski_broj = po_br
        self.grad = grad
        
    def create_brojilo(self):
        try:
            cursor = connection.cursor()
            cursor.execute("insert into brojilo (idbrojila, ime, prezime, ulica, broj, postbroj, grad)" + 
            " values (auto_inc.nextval, '" + self.ime + "','" + self.prezime + "','" + self.ulica + "','" + self.broj + "','" + str(self.postanski_broj) + "','" + self.grad + "')")

            connection.commit()
            return 'Uspesno sacuvan korisnik u bazi!'
        except Exception as e:
            print(e)