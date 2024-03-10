import os.path
import sys
import socket
import time

from largeFileScript import create_large_txt_file

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


def send_packet_and_wait_for_ack(sock, packet, packet_length, connection_type, address):
    while True:
        sock.send(packet.encode('utf-8'))
        sock.settimeout(2)
        try:
            if connection_type == 'UDP':
                ack, _ = sock.recvfrom(packet_length)
            else:
                ack = sock.recv(packet_length)
            if ack.decode('utf-8') == 'ACK':
                break
        except socket.timeout:
            print("No acknowledgment received, resending packet...")


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
    socket.connect((host, port))

    if len(sys.argv) >= 4:
        file_path = sys.argv[4]

    packet_length = int(sys.argv[2])
    if packet_length < 1 or packet_length > 65535:
        print("Packet length not valid, exiting.")
        exit(0)

    if os.path.exists(file_path):
        packets = split_file_into_packets(file_path, packet_length)
    else:
        packets = split_file_into_packets(create_large_txt_file(file_path, 500), packet_length)

    start_time = time.time()
    for idx, i in enumerate(packets):
        if transmission_mechanism == 1:
            socket.send(i.encode('utf-8'))
        else:
            send_packet_and_wait_for_ack(socket, i, packet_length, connection_type, host)
    if connection_type == 'UDP':
        socket.send('Done'.encode('utf-8'))
    end_time = time.time()

    print(f"Transmission time: {end_time-start_time} seconds")
    print(f"Client: {connection_type}, messages sent: {len(packets)}, bytes sent: {os.path.getsize('large.txt')}")
    socket.close()
