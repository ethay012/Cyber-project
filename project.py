# -*- coding: utf-8 -*-
import socket
import nmap
import random
import os
import paramiko
import re
from sshtunnel import SSHTunnelForwarder

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
    ssh = paramiko.SSHClient()
    pat = re.compile("Linux")
    ip = generate_ip()
    #ops = os.system('nmap -O -Pn ' + ip)
    #while re.search(pat, str(ops)) is not None:
     #   ip = generate_ip()
    tunnel(ssh, 'ip')
    ssh.close()


def tunnel(client, ip):
    """try:
        client.connect(ip, username=default[0][0], password=[0][0])
        print "Connection successful"
        trans = client.get_transport()
        trans.open_channel("forwarded-tcpip", dest_addr=('serverIP',8000), src_addr=('localhost'),8000)
    except socket.error:
        tunnel(client, '1ip')"""
    host = SSHTunnelForwarder(
        ip,
        ssh_username=default[0][0],
        ssh_password=default[0][1],
        remote_bind_address=('127.0.0.1', 443)
    )
    host.stop()


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
