#!/usr/bin/env/python

import scapy.all as scapy

def scan(ip):
    #can use the .summary method to get the summary of what the command is doing
    #can also use the scapy.ls() command to get the fields which can be changed.
    #.show() method can be used to show the contents of the packet
    arp_request_packet = scapy.ARP(pdst=ip)  # pdst is the destination ip or ip range to send request to
    braodcast_packet = scapy.Ether(dst="ff: ff: ff: ff: ff: ff") # setting variable to store ether packet with desitanation as broadcast MAC
    arp_request_broadcast_packet = braodcast_packet/arp_request_packet #merging both the ether and arp packet in one packet
    answered_list = scapy.srp(arp_request_broadcast_packet, timeout=1, verbose=False)[0] # index 0 contains the answered list.
    #scapy.srp() function is used to send the packets and it returns 2 lists. One is answered other is unanswered.
    clients_list = [] #creating empty dictionary
    for element in answered_list:#iterating over the contents of answered list which itself contains a tuple with our desired data at index 1.
        client_dict = {"IP": element[1].psrc, "MAC": element[1].hwsrc} #adding the ip address to key IP and MAC Address to the key MAC # .src is ip and .hwsrc is MAC #can use .show() method to see the data of element
        clients_list.append(client_dict) # appending the dictionary element to the list.
    return clients_list

def print_result(result_list): # defining a print fucntion to print the output.
    print("IP\t\t\tMAC Address")
    print("----------------------------------------------------")
    for client in result_list:
        print(client["IP"] + "\t\t" + client["MAC"])

print("[+] Enter the ip address range you want to scan for.")
ip = input("[+] ")
print("")
scan_result = scan(ip)
print_result(scan_result)
