#!/usr/bin/python3

import socket
import os
import sys
from termcolor import colored
import pyfiglet

# Function to grab the banner from a specific IP and port
def retBanner(ip, port):
    try:
        socket.setdefaulttimeout(2)  # Set a timeout for the socket
        with socket.socket() as sock:
            sock.connect((ip,port))  # Connect to the target IP and port
            banner = sock.recv(1024)  # Receive up to 1024 bytes
            return banner
    except:
        return  # Return None if connection fails

# Function to check if the banner matches any known vulnerabilities
def checkVulns(banner, vuln_lines):
    for line in vuln_lines:
        if line.strip() in banner:
            print(colored(f"[+] Server is vulnerable: {banner.strip()}", "red"))

def main():
    print(pyfiglet.figlet_format("VulnScanner", font="slant"))  # Print ASCII art banner
    # Check for correct usage and file accessibility
    if len(sys.argv) == 2:
        filename = sys.argv[1]
        if not os.path.isfile(filename):
            print("[-] File Doesn't Exist!")
            exit(0)
        if not os.access(filename, os.R_OK):
            print("[-] Access Denied!")
            exit(0)
        with open(filename, "r") as f:
            vuln_lines = f.readlines()  # Read all vulnerability signatures
    else:
        print(f"[-] Usage:  {sys.argv[0]} <vuln filename>")
        exit(0)

    # List of common ports to scan
    portlist = [21,22,25,80,110,443,445]
    # Loop through a range of IPs (currently only 192.168.204.131)
    for num in range(131,132):
        ip = "192.168.204." + str(num)
        print(f"checking {ip}")
        for port in portlist:
            banner = retBanner(ip, port)  # Attempt to grab the banner
            if banner:
                try:
                    banner_str = banner.decode('utf-8', errors='replace')  # Decode banner to string
                except:
                    banner_str = str(banner)
                print(colored(f"[+] {ip}/{port}: {banner_str.strip()}", "green"))  # Print the banner
                checkVulns(banner_str, vuln_lines)  # Check for vulnerabilities

if __name__ == "__main__":
    main()
