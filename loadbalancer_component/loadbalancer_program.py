from loadbalancer_class import LoadBalancer

if __name__ == '__main__':
    host = 'localhost'
    port = 8081
    loadbalancer = LoadBalancer(host=host, port=port)
    loadbalancer.start()