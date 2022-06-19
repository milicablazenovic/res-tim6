import sys
import unittest
import pickle
sys.path.append('../')
from unittest.mock import Mock, patch
from worker_component.worker_class import Worker


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