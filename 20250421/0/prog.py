import socket
import sys


def sqroots(coeffs:str) -> str:
    try:
        l = coeffs.split()
        if len(l) != 3 and l[0] == 0:
            raise ValueError
        else:
            a, b, c = map(int, coeffs.split())
            d = b * b - 4 * a * c
            if d == 0 or a == 0:
                return "1"
            if d > 0:
                return "2"
            if d < 0:
                return "0"
    except:
        TypeError



def sqrootnet(line, sock):
    sock.sendall((line + '\n').encode())
    return sock.recv(128).decode().strip()

if __name__ == '__main__':
    match sys.argv:
        case [prog, args]:
            print(sqroots(args))
        case [prog, args, host, port]:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(host, int(port))
                print(sqrootnet(args, s))
