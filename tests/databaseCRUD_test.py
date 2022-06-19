
import cx_Oracle
import sys
sys.path.append('../')
import database.databaseCRUD as databaseCRUD
from database.databaseCRUD import create_table, readUsers, db_connect, deleteUser, updateUser
import unittest, unittest.mock
from unittest.mock import Mock, patch 
from database.brojilo import Brojilo

class testdatabaseCRUD(unittest.TestCase):
    def setUp(self):
        global cursor, conn
        conn = db_connect("baza_test", "test", "localhost/xe")
        #conn = db_connect("PR1362018", "ftn", "localhost/xe")
        cursor = conn.cursor()
        
        create_table(conn)

    @patch('database.databaseCRUD.cx_Oracle')
    def test_db_connect(self, mock_sql):
        self.assertIs(databaseCRUD.cx_Oracle, mock_sql)

        #db_connect("PR1362018", "ftn", "localhost/xe")
        #mock_sql.connect.assert_called_with("PR1362018", "ftn", "localhost/xe")

        db_connect("baza_test", "test", "localhost/xe")
        mock_sql.connect.assert_called_with("baza_test", "test", "localhost/xe")

    def test_db_connect_input(self):

        db_connect("asdf", "qwer", "localhost")
        self.assertRaises(cx_Oracle.DatabaseError)
        db_connect("", "", "")
        self.assertRaises(cx_Oracle.DatabaseError)
        db_connect(True, False, True)
        self.assertRaises(TypeError)
        db_connect(1, 1, 1)
        self.assertRaises(TypeError)
        db_connect()
        self.assertRaises(cx_Oracle.DatabaseError)

    # Create ->
    def kreirajBrojilo_param(self, ime, prez, ul, br, po_br, grad): 
        brojilo = Brojilo('test_ime', 'test_prez', 'test_ul', 'test_br', 'test_po_br', 'test_grad' )
        brojilo = Brojilo(ime, prez, ul, br, po_br, grad)
        return brojilo
    
    def kreirajBrojilo(self):
        brojilo = Brojilo('test_ime', 'test_prez', 'test_ul', 'test_br', 'test_po_br', 'test_grad' )        
        return brojilo

    def test_createUser(self):
        brojilo = self.kreirajBrojilo()
        ret_val = brojilo.create_brojilo()
        self.assertRaises(Exception, ret_val)
        
        brojilo = self.kreirajBrojilo_param('', '', '', '', '', '')
        self.assertRaises(Exception, brojilo.create_brojilo())   

    def test_readUsers(self):
        # test kada nema redova u tabeli
        temp = readUsers()
        self.assertEqual(temp, "Tabela je prazna!")

        # test kada ima redova u tabeli
        cursor.execute("insert into brojilo values (auto_inc.nextval, 'pera', 'peric', 'gradska', 28, 31000, 'Uzice')")
        cursor.execute("insert into brojilo values (auto_inc.nextval, 'misa', 'misic', 'jevrejska', 15, 21000, 'Novi Sad')")
        conn.commit()

        temp = readUsers()
        self.assertEqual(temp, [(1, "pera", "peric", "gradska", 28, 31000, "Uzice"), (2, 'misa', 'misic', 'jevrejska', 15, 21000, 'Novi Sad')])

    def test_create_table(self):
        # test da li baca error kada se pokusa kreirati tabela sa istim imenom
        create_table(conn)
        self.assertRaises(cx_Oracle.DatabaseError)

        # test da li se tabele kreiraju kako treba
        cursor.execute("drop table potrosnja")
        cursor.execute("drop table brojilo")
        cursor.execute("drop sequence auto_inc")
        conn.commit()

        create_table(conn)
        query = """SELECT
            table_name
            FROM
            user_tables"""
        cursor.execute(query)
        result = cursor.fetchall()

        self.assertEqual(result, [('BROJILO',), ('POTROSNJA',)])
        
    def testUpdateUser(self):
        # azuriranje nepostojeceg brojila u sistemu
        self.assertRaises(Exception, updateUser(2, "pera", "peric", "gradska", 28, "31000", "Uzice"))
        
        # azuriranje postojecih brojila u sistemu
        cursor.execute("insert into brojilo values (auto_inc.nextval, 'pera', 'peric', 'gradska', 28, 31000, 'Uzice')")
        cursor.execute("insert into brojilo values (auto_inc.nextval, 'misa', 'misic', 'jevrejska', 15, 21000, 'Novi Sad')")
        conn.commit()
        self.assertEqual(updateUser(1, "pera", "peric", "gradska", 28, 31000, "Uzice"), "Uspesno ste izmenili korisnika")
        
        # nevalindi parametri
        self.assertRaises(Exception, updateUser("test", "pera", "peric", "gradska", 28, 31000, "Uzice"))
        self.assertRaises(Exception, updateUser(2, "pera", "peric", "gradska", "28", "31000", "Uzice"))
        self.assertRaises(Exception, updateUser(2, 22, 111, 333, 28, 31000, 234))


    def test_deleteUser(self):
        #test da li baca error kada pokusa da se obrise nepostojeci Id
        temp = deleteUser(2)        
        self.assertEqual(temp, "Greska, ne postoji ovaj Id u bazi!")
        

        cursor.execute("insert into brojilo values (auto_inc.nextval, 'pera', 'peric', 'gradska', 28, 31000, 'Uzice')")
        cursor.execute("insert into brojilo values (auto_inc.nextval, 'misa', 'misic', 'jevrejska', 15, 21000, 'Novi Sad')")
        conn.commit()

        #brisanje postojeceg Id-brisanje misa misic id=2         
        temp = deleteUser(2)
        temp2 = readUsers()
        self.assertEqual(temp, "Uspesno ste obrisali korisnika!")
        self.assertEqual(temp2, [(1, "pera", "peric", "gradska", 28, 31000, "Uzice")])
        
    def tearDown(self):
        cursor.execute("drop table potrosnja")
        cursor.execute("drop table brojilo")
        cursor.execute("drop sequence auto_inc")
        conn.commit()
        conn.close()
        
if __name__ == "__main__":
    unittest.main()