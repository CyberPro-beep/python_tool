#!/usr/bin/python

# Importing the relevant libraries needed for the project
from socket import *                # type: ignore # For network connections
from termcolor import colored       # For colored terminal output
import optparse                     # For command-line option parsing
from threading import *             # type: ignore # For threading support
import pyfiglet                     # For ASCII art banner

# Print ASCII art banner
print(pyfiglet.figlet_format("CARTWRIGHT", font="slant"))

# Function to scan a single port on the target host
def connScan(target_host, target_port):
    sock = None
    try:
        sock = socket(AF_INET, SOCK_STREAM)  # Create a TCP socket
        sock.connect((target_host, target_port))  # Attempt to connect to the port
        print(colored(f"[+] {target_port}/tcp is Open", "green"))  # Port is open
    except:
        print(colored(f"[-] {target_port}/tcp is Closed", "red"))  # Port is closed or unreachable
    finally:
        if sock:
            sock.close()  # Always close the socket

# Function to scan multiple ports on the target host
def portScan(target_host, target_ports):
    try:
        target_IP = gethostbyname(target_host)  # Resolve host to IP
    except:
        print(colored (f"[x] Can't resolve Target Name {target_host}", "red"))  # Hostname resolution failed
        return
    
    try:
        target_name = gethostbyaddr(target_IP)  # Attempt reverse DNS lookup
        print(f"[+] Scan Result for: {target_name[0]}")
    except:
        print(f"[+] Scan Result for: {target_IP}")  # If reverse lookup fails, print IP
    
    setdefaulttimeout(1)  # Set default socket timeout
    threads = []
    for target_port in target_ports:
        t = Thread(target=connScan, args=(target_host, int(target_port)))  # Create a thread for each port scan
        t.start()  # Start the thread
        threads.append(t)  # Keep track of threads
    for t in threads:
        t.join()  # Wait for all threads to finish

# Main function to parse arguments and start the scan
def main():
    parser = optparse.OptionParser("-H <target host> -P <target port>")
    parser.add_option("-H", dest="target_host", type="string", help="[*] Specify target host IP")
    parser.add_option("-P", dest="target_port", type="string", help="[*] Specify target ports separated by comma")
    (options, args) = parser.parse_args()
    target_host = options.target_host
    target_ports = str(options.target_port).split(',')  # Split ports by comma
    if not target_host or not target_ports or target_ports == ['']:
        print(parser.usage)
        print(colored("[x] Exiting Program...","red"))
        exit(0)
    portScan(target_host, target_ports)  # Start scanning
    exit(0)

# Entry point of the script
if  __name__ == '__main__':
    main()