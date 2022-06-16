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
        
        create_table(conn)

    def test_readUsers(self):
        # test kada nema redova u tabeli
        temp = readUsers()
        self.assertEqual(temp, "Tabela je prazna!")

        # test kada ima redova u tabeli
        cursor.execute("insert into brojilo values (1, 'pera', 'peric', 'gradska', 28, 31000, 'Uzice')")
        cursor.execute("insert into brojilo values (2, 'misa', 'misic', 'jevrejska', 15, 21000, 'Novi Sad')")
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
        conn.commit()

        create_table(conn)
        query = """SELECT
            table_name
            FROM
            user_tables"""
        cursor.execute(query)
        result = cursor.fetchall()

        self.assertEqual(result, [('BROJILO',), ('POTROSNJA',)])
        
    def tearDown(self):
        cursor.execute("drop table potrosnja")
        cursor.execute("drop table brojilo")
        conn.commit()
        conn.close()