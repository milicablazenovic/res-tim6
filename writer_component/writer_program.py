from writer_class import Writer

if __name__ == '__main__':
    host = 'localhost'
    port = 8081
    writer = Writer(host=host, port=port)
    writer.start()
    