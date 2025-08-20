#!/usr/bin/python3

import socket

# Function to grab the banner from a specific IP and port
def retBanner(ip, port):
    try:
        socket.setdefaulttimeout(2)  # Set a timeout for the socket connection
        with socket.socket() as sock:
            sock.connect((ip, port))  # Connect to the target IP and port
            banner = sock.recv(1024)  # Receive up to 1024 bytes from the socket
            return banner
    except:
        return  # Return None if connection fails or times out

def main():
    ip = input("Enter Target IP: ")  # Prompt user for the target IP address
    for port in range(1, 65353):  # Scan ports from 1 to 65352
        banner = retBanner(ip, port)  # Attempt to grab the banner for each port
        if banner:
            try:
                banner_str = banner.decode('utf-8', errors='replace').strip()  # Decode banner to string
            except:
                banner_str = str(banner)  # Fallback to string representation if decoding fails
            print(f"[+] {ip}/{port} - {banner_str}")  # Print the banner information

if __name__ == "__main__":
    main()  # Run the main function if the script is executed directly