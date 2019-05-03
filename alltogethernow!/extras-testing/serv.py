while True:
    try:
        import socket

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('127.0.0.1', 1003))
        server.listen(1)
        while True:
            connection, address = server.accept()
            print('Got connection from', address)
            connection.send('Welcome to the TCP listener'.encode())
            
            while True:
                try:
                    data = connection.recv(1024).decode()
                    if not data:
                        continue
                    print(data)
                    connection.send(data.encode())
                except ConnectionResetError as e:
                    connection.close()

    except Exception as e:
        print(e)
        while True:
            continue
    
