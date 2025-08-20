#!/usr/bin/python

import socket
from termcolor import colored

host = input("[*] Enter the IP address of system you want to scan it's port: ")
# port = int(input("[*] Enter the port to scan: "))

def port_scanner(port):
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.settimeout(1)
    if connection.connect_ex((host, port)):
        print(colored(f"[x] Port {port} is Closed", "red"))
    else:
        print(colored(f"[+] Port {port} is Opened", "green"))
    connection.close()

for port in range(1, 1000):
    port_scanner(port)
