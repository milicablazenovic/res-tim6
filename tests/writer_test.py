from datetime import datetime
from multiprocessing.sharedctypes import Value
import sys
import unittest
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