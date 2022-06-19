import sys
import unittest
sys.path.append('../')
import random
from unittest.mock import Mock
from loadbalancer_component.loadbalancer_class import LoadBalancer

class testLoadBalancer(unittest.TestCase):
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

    