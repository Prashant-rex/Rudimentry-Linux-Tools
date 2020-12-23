import subprocess
import re

class MAC_CHANGER:
    def __init__(self):
        self.MAC = ""  # defining an empty variable

    def get_MAC(self , interface):  # function to get the current MAC of the interface
        output = subprocess.run(["ifconfig", interface], shell = False, capture_output = True) # running the ifconfig command and storing the output in variable.

        console_result = output.stdout.decode("UTF-8") # formatting the output as UTF-8

        mac_pattern = r'ether\s[\da-f]{2}:[\da-f]{2}:[\da-f]{2}:[\da-f]{2}:[\da-f]{2}:[\da-f]{2}' # regex to match MAC Address pattern from the output
        regex = re.compile(mac_pattern)
        mac_string = regex.search(console_result)

        current_mac = mac_string.group().split(" ")[1]

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
x = mc.get_MAC("eth0") # calling the get_mac function and assigning the returned MAC to variable x.

print("[+] Current MAC Address is", x) # prints the current MAC
print("[+] Enter the desired MAC Address ") 
fake_mac = input("[+] ") # prompts the user to give a desired MAC
is_valid = mc.check_valid(fake_mac) # checks whether MAC is of proper Format and assigns a boolen to is_valid. 

if(is_valid):
    print("[+] Changing MAC Address.") # if true
    y = mc.change_MAC("eth0", fake_mac) #calls the change_MAC function
    print("[+] New MAC Address is",y) # prints the New MAC Address.



