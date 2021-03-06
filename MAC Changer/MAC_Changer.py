#!/usr/bin/env/python

import subprocess
import re

class MAC_CHANGER:
    def __init__(self):
        self.MAC = ""  # defining an empty variable

    def validate_iface(self, iface): # to validate interface name
        if(iface == "eth0"):
            return True
        elif(iface == "ens33"):
            return True
        elif(iface == "enp0s3"):
            return True
        elif(iface == "wlan0"):
            return True
        else:
            return False
        

    def get_MAC(self , interface):  # function to get the current MAC of the interface
        output = subprocess.run(["ifconfig", interface], shell = False, capture_output = True) # running the ifconfig command and storing the output in variable.

        console_result = output.stdout.decode("UTF-8") # formatting the output as UTF-8

        mac_pattern = r'ether\s[\da-f]{2}:[\da-f]{2}:[\da-f]{2}:[\da-f]{2}:[\da-f]{2}:[\da-f]{2}' # regex to match MAC Address pattern from the output
        regex = re.compile(mac_pattern)
        mac_string = (regex.search(console_result))
        if (mac_string is None):
            print("[-] Select appropriate interface.")
            exit()
        else:
            current_mac = (mac_string.group().split(" ")[1])
            self.MAC = current_mac # assigning the current MAC value to variable    
            return current_mac

    def change_MAC(self, interface, new_mac): # function to change the MAC address of the interface.
        
        interface_down = subprocess.run(["ifconfig", interface, "down"], shell=False, capture_output=True) # command to switch the interface off
        if(interface_down.stderr.decode("UTF-8")):  # if some system error in performing the above step print a warning.
            print(interface_down.stderr.decode("UTF-8"))

        change_mac = subprocess.run(["ifconfig", interface, "hw", "ether", new_mac], shell=False, capture_output=True) # command to change the current MAC to the MAC provided by new_mac
        if(change_mac.stderr.decode("UTF-8")):  # if some system error in performing the above step print a warning.
            print(change_mac.stderr.decode("UTF-8"))  

        interface_up = subprocess.run(["ifconfig", interface, "up"], shell=False, capture_output=True) # command to re-enable the network interface with new MAC.
        if(interface_up.stderr.decode("UTF-8")):  # if some system error in performing the above step print a warning.
            print(interface_up.stderr.decode("UTF-8"))

        return self.get_MAC(interface) # calls the get_MAC function and returns the new MAC.

    def check_valid(self, fake_mac): # function to check whether the new MAC provided is of valid syntax
        valid = bool(re.match(r'[\da-f]{2}:[\da-f]{2}:[\da-f]{2}:[\da-f]{2}:[\da-f]{2}:[\da-f]{2}', fake_mac)) # regex to compare the fake_mac is of suitable format.

        if(valid):
            print("[+] Entered MAC Address is Valid.")
            return True
        else:
            print("[-] Bad Input!!!") # if unsuitable prompt the user of BAD Input !!!
            print("[-] Enter the MAC in the format of XX:XX:XX:XX:XX:XX")
            return False


mc = MAC_CHANGER() # creating object of MAC_CHANGER class

print("[+] Specify the Network Interface. Run ifconfig if you don't know.")
iface = input("[+] ")
iface_valid = mc.validate_iface(iface) # to check whether the interface name provided is from the default lists

if(iface_valid):
    x = mc.get_MAC(iface) # calling the get_mac function and assigning the returned MAC to variable x.
    print("[+] Current MAC Address " + iface + " is", x) # prints the current MAC
    print("[+] Enter the desired MAC Address ") 
    fake_mac = input("[+] ") # prompts the user to give a desired MAC
    is_valid = mc.check_valid(fake_mac) # checks whether MAC is of proper Format and assigns a boolen to is_valid. 

    if(is_valid):
        print("[+] Changing MAC Address.") # if true
        y = mc.change_MAC(iface, fake_mac) #calls the change_MAC function
        print("[+] New MAC Address is",y) # prints the New MAC Address.
else:
    print("[-] Check the name of the interface with internet connectivity.")

