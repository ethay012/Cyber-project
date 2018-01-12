# -*- coding: utf-8 -*-
import socket, nmap


def menu():
    return """1. Get IPs list.
    2. Get information about a device.
    3. Tunnel through device.
    4. Exit.
    (1/2/3/4)
    """


def get_list():
    return [ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")]


#def Get_Info():


#def Tunnel():


def handle(ans, client):
    if ans == 1:
        print ', '.join(get_list())



def check(ans):
    return ans in [1, 2, 3]


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ans = input(menu())
    while ans != 4:
        if check(ans):
            handle(ans, client)
        else:
            print "Invalid request"
        ans = input(menu())
    client.close()


if __name__ == '__main__':
    main()
