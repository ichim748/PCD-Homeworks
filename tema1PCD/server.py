import sys
import socket

connection_type = 'none'

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Usage: <Protocol> <Buffer Size> <Transmission Mechanism>")
        exit(1)

    host = socket.gethostname()
    port = 6787

    if sys.argv[3].lower() == 'streaming':
        transmission_mechanism = 1
    elif sys.argv[3].lower() == 'stop-and-wait':
        transmission_mechanism = 0
    else:
        print("Invalid transmission mechanism. Choose 'streaming' or 'stop-and-wait'.")
        exit(1)

    if sys.argv[1].upper() == 'TCP':
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection_type = 'TCP'
    elif sys.argv[1].upper() == 'UDP':
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        connection_type = 'UDP'
    else:
        print("Invalid protocol. Choose 'TCP' or 'UDP'.")
        exit(1)

    server_socket.bind((host, port))
    print(f'Server listening on {host}:{port} ({connection_type})')

    if connection_type == 'TCP':
        server_socket.listen(1)

    while True:
        connection = None
        number_of_messages_read = 0
        number_of_bytes_read = 0

        if connection_type == 'TCP':
            connection, address = server_socket.accept()

        with open('received_data.txt', 'a') as file:
            while True:
                data = b''
                if connection_type == 'TCP':
                    data = connection.recv(int(sys.argv[2]))
                    if transmission_mechanism == 0:
                        connection.send('ACK'.encode('utf-8'))
                else:
                    data, address = server_socket.recvfrom(int(sys.argv[2]))
                    if transmission_mechanism == 0:
                        server_socket.sendto('ACK'.encode('utf-8'), address)

                if data:
                    message = data.decode('utf-8')
                    if message != 'Done' and message != 'ACK':
                        file.write(message + '\n')
                        number_of_messages_read += 1
                        number_of_bytes_read += len(data)
                    else:
                        break

        print(f"Data written to file 'received_data.txt'")
        print(f"Server session: {connection_type}, messages read: {number_of_messages_read}, bytes read: {number_of_bytes_read}")

        if connection_type == 'TCP' and connection:
            connection.close()
