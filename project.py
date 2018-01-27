# -*- coding: utf-8 -*-
import socket
import nmap
import random
import os
import paramiko


default = [("ubuntu", ""), ("admin", "password")]


def menu():
    return """1. Get IPs list.
2. Get information about a device.
3. Tunnel through device.
4. Exit.
(1/2/3/4)
"""


def get_list():
    nm = nmap.PortScanner()
    nm.scan()
    return nm.all_hosts()


def get_info():
    ip = raw_input("Insert ip: ")
    return os.system('nmap -O -Pn ' + ip)


def generate_ip():
    str_ip = "77."
    int_ip = random.randint(124, 127)
    str_ip += str(int_ip) + '.'
    int_ip = random.randint(0, 255)
    str_ip += str(int_ip) + '.'
    int_ip = random.randint(0, 255)
    str_ip += str(int_ip)
    print str_ip
    return str_ip


def init_tunnel():
    ip = generate_ip()
    ssh = paramiko.SSHClient()
    tunnel(ssh, ip)
    ssh.close()


def tunnel(client, ip):
    try:
        client.connect(ip, port=22, username=default[0][0], password=[0][0])
        stdin, stdout, stderr = client.exec_command('ls')
        print stdout
        print "Connection successful"
    except socket.error:
        tunnel(client, '192.168.56.1')


def handle(ans, client):
    if ans == 1:
        print get_list()
    if ans == 2:
        print get_info()
    if ans == 3:
        init_tunnel()


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
