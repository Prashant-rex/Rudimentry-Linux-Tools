#!/usr/bin/env/python

import scapy.all as scapy

def scan(ip):
    arp_request_packet = scapy.ARP(pdst=ip)  # pdst is the destination ip or ip range to send request to
    #can use the .summary method to get the summary of what the command is doing
    #can also use the scapy.ls() command to get the fields which can be changed.
    #.show() method can be used to show the contents of the packet
    braodcast_packet = scapy.Ether(dst="ff: ff: ff: ff: ff: ff") # setting variable to store ether packet with desitanation as broadcast MAC
    arp_request_broadcast_packet = braodcast_packet/arp_request_packet #merging both the ether and arp packet in one packet
    answered_list = scapy.srp(arp_request_broadcast_packet, timeout=1, verbose=False)[0] # index 0 contains the answered list.
    #scapy.srp() function is used to send the packets and it returns 2 lists. One is answered other is unanswered.

    print("IP\t\t\tMAC Address")
    print("----------------------------------------------------")

    for element in answered_list:  #iterating over the contents of answered list which itself contains a tuple with our desired data at index 1.
        #can use .show() method to see the data of element
        print(element[1].psrc + "\t\t" + element[1].hwsrc) # .src is ip and .hwsrc is MAC
print("[+] Enter the ip address range you want to scan for.")
ip = input("[+] ")
print("")
scan(ip)