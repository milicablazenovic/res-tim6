import sys
sys.path.append('../')
from database.databaseCRUD import create_table, readUsers, db_connect
import unittest, unittest.mock
import cx_Oracle 

class testdatabaseCRUD(unittest.TestCase):
    def setUp(self):
        global cursor, conn
        conn = db_connect("baza_test", "test", "localhost/xe")
        cursor = conn.cursor()
        
        # TODO: odraditi drop tabela sa oracle sintaksom
        #cursor.execute("drop table if exists potrosnja")
        #cursor.execute("drop table if exists brojilo")
        
        create_table(conn)
        cursor.execute("delete from brojilo")
        cursor.execute("delete from potrosnja")

        conn.commit()
    def test_readUsers(self):
        temp = readUsers()
        self.assertEqual(temp, "Tabela je prazna!")

        cursor.execute("insert into brojilo values (1, 'pera', 'peric', 'gradska', 28, 31000, 'Uzice')")
        cursor.execute("insert into brojilo values (2, 'misa', 'misic', 'jevrejska', 15, 21000, 'Novi Sad')")
        conn.commit()

        temp = readUsers()
        self.assertEqual(temp, [(1, "pera", "peric", "gradska", 28, 31000, "Uzice"), (2, 'misa', 'misic', 'jevrejska', 15, 21000, 'Novi Sad')])


    def tearDown(self):
        conn.close()