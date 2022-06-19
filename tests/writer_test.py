from datetime import datetime
from multiprocessing.sharedctypes import Value
from re import T
from socket import socket
import sys
import unittest
import socket
from unittest.mock import Mock
sys.path.append('../')
from writer_component.writer_class import Writer

class testWriter(unittest.TestCase):
    def test_data_input_format(self):
        writer = Writer('localhost', 8081)
        # ispravni parametri
        result = writer.data_input_format(5, 1540)
        dt = datetime.now()
        time_stamp = dt.strftime('%X %x')
        self.assertEqual(result, time_stamp + ' - 5 : 1540')

        # neispravni parametri 
        self.assertRaises(Exception, writer.data_input_format(5.5, 1540))
        self.assertRaises(Exception, writer.data_input_format("5.5", 1540))
        self.assertRaises(Exception, writer.data_input_format(7, "asdf"))
        self.assertRaises(Exception, writer.data_input_format(7, ""))
        self.assertRaises(Exception, writer.data_input_format("", 1540))
        self.assertRaises(Exception, writer.data_input_format(-7, 1540))
        self.assertRaises(Exception, writer.data_input_format(-9, -6000))
        self.assertRaises(Exception, writer.data_input_format(3, -9000))
        
        writer.close_socket()
        
    def test_connect_socket_wrong_params(self):        
        writer = Writer('tttt', 8081)
        self.assertRaises(TypeError, writer.connect_socket())
        writer.close_socket()
        writer = Writer('localhost', '8081')
        self.assertRaises(TypeError, writer.connect_socket())
        writer.close_socket()
    
    """###
    def test_sent(self):
        writer = Writer('localhost', 8081)
        connection = Mock()
        self.assertAlmostEqual(writer.send("poruka", connection), (connection.recv.return_value,True))
        connection.recv.return_value = None
        self.assertAlmostEqual(writer.send("poruka", connection), ('Nema odgovora', False))
        writer.close_socket()
    """
        
if __name__ == "__main__":
    unittest.main()
        