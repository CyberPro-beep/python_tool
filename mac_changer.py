#!/bin/bash

import subprocess
import re

def vaild_mac_address(mac):
    # vaild the mac address
    # Validate MAC address format (e.g., 00:11:22:33:44:55)
    pattern = r"^([0-9A-Fa-f]{2}:){5}([0-9A-Fa-f]{2})$"
    return re.match(pattern, mac) is not None

def change_mac_address(mac, interface):
    # changes the mac address
    new_mac = mac
    interface = interface

    try:
        subprocess.run(["sudo", "ifconfig", interface, "down"], check=True)
        subprocess.run(["sudo", "ifconfig", interface, "hw", "ether", new_mac], check=True)
        subprocess.run(["sudo", "ifconfig", interface, "up"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error changing MAC address: {e}")
        exit(1)

def comfirm_change(mac, interface):
    # Confirm MAC address change
    try:
        result = subprocess.run(["ifconfig", interface], capture_output=True, text=True, check=True)
        match = re.search(r"ether ([0-9a-fA-F:]{17})", result.stdout)
        if match:
            current_mac = match.group(1)
            return current_mac.lower() == mac.lower()
        return False
    except subprocess.CalledProcessError as e:
        print(f"Error confirming MAC address: {e}")
        return False


if __name__ == '__main__' :
    import argparse
    try:
        parser = argparse.ArgumentParser(description="Change MAC address of a network interface.")
        parser.add_argument("-i", "--interface", required=True, help="Network interface (e.g., eth0)")
        parser.add_argument("-m", "--mac", required=True, help="New MAC address (e.g., 00:11:22:33:44:55)")
        args = parser.parse_args()
    except Exception as e:
        print(f"Argument parsing error: {e}")
        exit(1)

    if not vaild_mac_address(args.mac):
        print(f"Invalid MAC address format: {args.mac}")
        exit(1)

    print(f"Changing MAC address for {args.interface} to {args.mac}...")
    change_mac_address(args.mac, args.interface)
    if comfirm_change(args.mac, args.interface):
        print(f"MAC address changed successfully to {args.mac} on {args.interface}.")
    else:
        print("Failed to change MAC address.")