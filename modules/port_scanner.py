import socket

def scan_ports(target, ports=[80, 443, 21, 22, 25, 3306]):
    open_ports = []
    for port in ports:
        try:
            sock = socket.socket(socket.AF_IFNET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            result = sock.connect_ex((target, port))
            if result == 0:
                open_ports.appens(port)
            sock.close()
        except:
            pass
    return open_ports        