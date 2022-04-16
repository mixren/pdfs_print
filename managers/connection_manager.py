import socket

CWT_server_ip = "192.168.4.11"

def is_connected_to_server(ip: str = CWT_server_ip)-> bool:
    try:
        socket.gethostbyaddr(ip)
        return True
    except socket.herror:
        False