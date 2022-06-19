from os import curdir
import sys
import unittest
import pickle
sys.path.append('../')
from unittest.mock import Mock, patch
from worker_component.worker_class import Worker
from database.databaseCRUD import db_connect, create_table, db_disconnect

class testWorker(unittest.TestCase):
    @patch('worker_component.worker_class.socket.socket')
    def test_revfrom(self, tcp_socket):
        worker = Worker('localhost', 8082)
        worker.recieve_data(tcp_socket)
        
        tcp_socket.recvfrom.assert_called()
        tcp_socket.recvfrom.assert_called_with(1024)
        worker.close_socket()

    @patch('worker_component.worker_class.pickle')
    def test_pickle_loads(self, pickle):
        worker = Worker('localhost', 8082)
        worker.load_data("")
        pickle.loads.assert_called()
        worker.close_socket()
    
    def test_save_data(self):
        worker = Worker('localhost', 8082)

        # radimo sa fejk bazom 

        conn = db_connect("baza_test", "test", "localhost/xe")
        create_table(conn)
        cursor = conn.cursor()
        cursor.execute("insert into brojilo values (auto_inc.nextval, 'pera', 'peric', 'gradska', 28, 31000, 'Uzice')")
        cursor.execute("insert into brojilo values (auto_inc.nextval, 'misa', 'misic', 'jevrejska', 15, 21000, 'Novi Sad')")
        cursor.execute("insert into brojilo values (auto_inc.nextval, 'pera', 'peric', 'gradska', 28, 31000, 'Uzice')")
        cursor.execute("insert into brojilo values (auto_inc.nextval, 'misa', 'misic', 'jevrejska', 15, 21000, 'Novi Sad')")

        # sve vrednosti validne, sve ih upisuje
        data = [{1: 123}, {2: 345}, {3: 6325}, {4:7985}]
        result = worker.save_data(data, conn)
        cursor.execute("select mesec from potrosnja")
        rows = cursor.fetchall()

        
        self.assertEqual(result,[{1: 123}, {2: 345}, {3: 6325}, {4:7985}])

        # test da li je mesec pravilno upisan
        self.assertEqual(rows, [(1,), (1,), (1,), (1,)])

        # validne vrednosti su {2: 345} i {4:346}
        data = [{111: 123}, {2: 345}, {75:456}, {78:234}, {4:346}, {62:435}, {0:234}]
        result = worker.save_data(data, conn)
        cursor.execute("select mesec from potrosnja")
        rows = cursor.fetchall()

        self.assertEqual(result, [{2: 345}, {4:346}])

        # test da li je mesec pravilno upisan
        self.assertEqual(rows, [(1,), (1,), (1,), (1,), (2,), (2,)])

        # nijedna vrednost nije validna
        data = [{111: 123}, {22: 345}, {75:456}, {78:234}, {55:346}, {62:435}, {0:234}]
        result = worker.save_data(data, conn)

        self.assertEqual(result, [])


        # dropujemo tabele test baze
        cursor.execute("drop table potrosnja")
        cursor.execute("drop table brojilo")
        cursor.execute("drop sequence auto_inc")
        conn.commit()

        worker.close_socket()