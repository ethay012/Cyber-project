# -*- coding: utf-8 -*-
import socket
import nmap
import random
import os
import re
import subprocess
from selenium import webdriver


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


def chec_if_up(ip):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect_ex((ip, 22))
        sock.shutdown(2)
        result = True
    except:
        result = False
    print result
    return result


def init_tunnel():
    ans = raw_input("Generate ip [Y/N]? ")
    pat = re.compile("Linux")
    if ans.upper() == 'Y':
        ip = generate_ip()
        ops = ""
        if chec_if_up(ip):
            ops = os.system('nmap -O --osscan-guess ' + ip)
        while re.search(pat, str(ops)) is None:
            ip = generate_ip()
            if chec_if_up(ip):
                ops = os.system('nmap -O --osscan-guess ' + ip)
    else:
        ip = raw_input("Insert ip: ")
        ops = ""
        if chec_if_up(ip):
            ops = os.system('nmap -O --osscan-guess ' + ip)
        while re.search(pat, str(ops)) is None:
            ip = raw_input("Insert another ip: ")
            if chec_if_up(ip):
                ops = os.system('nmap -O --osscan-guess ' + ip)
    tunnel_putty_link(ip)


def install_firefox_proxy(PROXY_HOST,PROXY_PORT):
    fp = webdriver.FirefoxProfile()
    fp.set_preference("network.proxy.type", 1)
    fp.set_preference("network.proxy.socks", PROXY_HOST)
    fp.set_preference("network.proxy.socks_port", int(PROXY_PORT))
    fp.set_preference("network.proxy.socks_remote_dns", True)
    fp.update_preferences()
    return webdriver.Firefox(firefox_profile=fp)


def tunnel_putty_link(ip):
    driver = install_firefox_proxy("127.0.0.1", 3200)
    driver.get('about:config')
    with open('login.txt', 'r') as details:
        for line in details:
            read_line = line.split(',')
            name = read_line[0]
            password = read_line[1][1:].replace('-', '')
            try:
                command = "plink -D 3200 -pw %s %s@%s" % (password, name, ip)  # the shell command
                print subprocess.check_output(command)
            except Exception as err:
                print "an error occured: " + str(err)


def handle(ans):
    if ans == 1:
        print get_list()
    if ans == 2:
        print get_info()
    if ans == 3:
        init_tunnel()


def check(ans):
    return ans in [1, 2, 3]


def main():
    tunnel_putty_link(ip)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ans = input(menu())
    while ans != 4:
        if check(ans):
            handle(ans)
        else:
            print "Invalid request"
        ans = input(menu())
    client.close()


if __name__ == '__main__':
    main()
