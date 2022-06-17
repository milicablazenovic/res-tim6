from loadbalancer_class import LoadBalancer

if __name__ == '__main__':
    host = 'localhost'    
    port = 8081

    host2 = 'localhost'
    port2 = 8082
    
    loadbalancer = LoadBalancer(host=host, port=port, host2=host2, port2=port2)
    loadbalancer.start()