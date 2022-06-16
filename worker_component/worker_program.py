from worker_class import Worker

if __name__ == '__main__':
    host = 'localhost'
    port = 8081
    worker = Worker(lb_host=host, lb_port=port)
    worker.start()