import sys
import socket
import time

connection_type = 'none'


def split_file_into_packets(filename, packet_size):
    packets = []
    with open(filename, 'r') as f:
        while True:
            chunk = f.read(packet_size)
            if not chunk:
                break
            packets.append(chunk)
    return packets


if __name__ == '__main__':
    if len(sys.argv) < 3:
        exit(0)
    host = socket.gethostname()
    port = 6787
    if sys.argv[1] == 'TCP':
        socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection_type = 'TCP'
    else:
        socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        connection_type = 'UDP'
    socket.connect((host, port))

    # functie de luat cv fisier, impartit si trimis pe bucati si numarat bucatile
    packet_length = int(sys.argv[2])
    packets = split_file_into_packets('large.txt', packet_length)
    for idx, i in enumerate(packets):
        socket.send(i.encode('utf-8'))
    if connection_type == 'UDP':
        socket.send('Done'.encode('utf-8'))
    print(f"Client: {connection_type}, messages sent: {len(packets)}, bytes read: {packet_length * len(packets)}")
    socket.close()
