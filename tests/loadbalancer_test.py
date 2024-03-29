import os
import sys
sys.path.append('../')
import unittest
import random
from unittest.mock import Mock
import sys
from loadbalancer_component.loadbalancer_class import LoadBalancer

class testLoadBalancer(unittest.TestCase):

    # forward_data()
    def test_forwarded_10_values_to_worker(self):
        loadbalancer = LoadBalancer('localhost', 8081, 'localhost', 8082)
        connection = Mock()
        data = [{1: 123}, {2: 345}, {3:456}, {4:234}, {5:346}, {6:435}, {7:234}, {8:234}, {9:234}, {10:234}]
        self.assertEqual(loadbalancer.forward_data(data,connection), True)

        loadbalancer.close_sockets()

    def test_load_balancer_wont_forward_strings(self):
        loadbalancer = LoadBalancer('localhost', 8081, 'localhost', 8082)
        connection = Mock()
        data = 'neki string'
        self.assertEqual(loadbalancer.forward_data(data, connection), 'Neispravna lista!')

        loadbalancer.close_sockets()

    def test_load_balancer_wont_forward_booleans(self):
        loadbalancer = LoadBalancer('localhost', 8081, 'localhost', 8082)
        connection = Mock()
        data = False
        self.assertEqual(loadbalancer.forward_data(data, connection), 'Neispravna lista!')

        loadbalancer.close_sockets()

    def test_load_balancer_wont_forward_integers(self):
        loadbalancer = LoadBalancer('localhost', 8081, 'localhost', 8082)
        connection = Mock()
        data = 13123
        self.assertEqual(loadbalancer.forward_data(data, connection), 'Neispravna lista!')

        loadbalancer.close_sockets()

    def test_load_balancer_wont_forward_dictionary(self):
        loadbalancer = LoadBalancer('localhost', 8081, 'localhost', 8082)
        connection = Mock()
        data = {1: 13}
        self.assertEqual(loadbalancer.forward_data(data, connection), 'Neispravna lista!')

        loadbalancer.close_sockets()

    def test_load_balancer_wont_forward_list_with_elements_that_are_not_dictionary(self):
        loadbalancer = LoadBalancer('localhost', 8081, 'localhost', 8082)
        connection = Mock()
        data = [{1: 13}, 5, 'string', 1, 1, 1, 1, 1, 1, 1]
        self.assertEqual(loadbalancer.forward_data(data, connection), 'Neispravni elementi u listi!')

        loadbalancer.close_sockets()

    def test_load_balancer_doesnt_send_data_if_not_10_elements(self):
        loadbalancer = LoadBalancer('localhost', 8081, 'localhost', 8082)
        connection = Mock()
        data = []
        for el in range(9):
            index = el+1
            value = random.randint(1,1000)
            data.append({index: value})
            self.assertEqual(loadbalancer.forward_data(data, connection), 'Nema 10 vrednosti u listi!')

        loadbalancer.close_sockets()

    # parse_data()
    def test_parse_data(self):
        loadbalancer = LoadBalancer('localhost', 8081, 'localhost', 8082)

        line_array = []
        for i in range(10):
            line_array.append(f'14:14:13 06/19/22 - {i+1} : 6688' + '\n')

        list_of_dictionaries = []
        self.assertEqual(loadbalancer.parse_data(list_of_dictionaries, line_array), 'Uspesno parsirani podaci!')

        loadbalancer.close_sockets()

    # receive_data()
    def test_receive_data(self):
        loadbalancer = LoadBalancer('localhost', 8001, 'localhost', 8002)

        data = "15:32:00 06/19/22 - 68 : 533"
        self.assertEqual(loadbalancer.receive_data(data, 'buffer_test.txt'), 'Uspesno upisan podatak u fajl!')
        os.remove('buffer_test.txt')

        loadbalancer.close_sockets()

    def test_dont_receive_empty_string(self):
        loadbalancer = LoadBalancer('localhost', 8001, 'localhost', 8002)

        data = ""
        self.assertEqual(loadbalancer.receive_data(data, 'buffer_test.txt'), 'Greska, podatak ne moze biti prazan string!')

        loadbalancer.close_sockets()

    def test_dont_receive_bool_data(self):
        loadbalancer = LoadBalancer('localhost', 8081, 'localhost', 8082)

        data= False
        self.assertEqual(loadbalancer.receive_data(data, 'buffer_test.txt'), 'Greska, neodgovarajuci tip!')

        loadbalancer.close_sockets()

    def test_dont_receive_int_data(self):
        loadbalancer = LoadBalancer('localhost', 8081, 'localhost', 8082)

        data = 1
        self.assertEqual(loadbalancer.receive_data(data, 'buffer_test.txt'), 'Greska, neodgovarajuci tip!')

        loadbalancer.close_sockets()

if __name__ == "__main__":
    unittest.main()