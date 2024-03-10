import sys
import socket


connection_type = 'none'


if __name__ == '__main__':
    if len(sys.argv) < 3:
        exit(0)
    host = socket.gethostname()
    port = 6787

    if sys.argv[3].lower() == 'streaming':
        transmission_mechanism = 1
    elif sys.argv[3].lower() == 'stop-and-wait':
        transmission_mechanism = 0

    if sys.argv[1] == 'TCP':
        socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection_type = 'TCP'
    else:
        socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        connection_type = 'UDP'

    socket.bind((host, port))
    print(f'Server listening on {host}:{port} ({connection_type})')

    if connection_type == 'TCP':
        socket.listen(1)
    while True:
        if connection_type == 'TCP':
            connection, address = socket.accept()
        number_of_messages_read = 0
        number_of_bytes_read = 0
        while True:
            if connection_type == 'TCP':
                data = connection.recv(int(sys.argv[2]))
                if transmission_mechanism == 0:
                    connection.send('ACK'.encode('utf-8'))
            else:
                data, address = socket.recvfrom(int(sys.argv[2]))
                if transmission_mechanism == 0:
                    socket.sendto('ACK'.encode('utf-8'), address)
            if data and data.decode('utf-8') != 'Done' and data.decode('utf-8') != 'ACK':
                number_of_messages_read += 1
                number_of_bytes_read += len(data)
            else:
                break
        print(f"Server session: {connection_type}, messages read: {number_of_messages_read}, bytes read: {number_of_bytes_read}")
        if connection_type == 'TCP':
            connection.close()
