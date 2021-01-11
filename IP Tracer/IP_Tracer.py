#!/usr/bin/env python3

import requests
import json

class Tracer():

    def get_domain(self):
        print("[+] Enter the IP Address or name of Website you want to know details of.")
        self.ip = input("[+] ")
        return self.ip

    def make_full_url(self):
        self.url = "http://ip-api.com/json/" + self.ip  #combining the provided ip with api to form the full url.

    def get_data(self):
        self.response = requests.get(self.url) #sending get request to the url.
        #http://ip-api/json/192.168.0.1
        self.data = json.loads(self.response.content)  #getting the content of the json file.
    
    def present_data(self): # presenting data
        print("")
        print("\t[+] IP       \t\t", self.data["query"])
        print("\t[+] CITY     \t\t", self.data["city"])
        print("\t[+] ISP      \t\t", self.data["isp"])
        print("\t[+] COUNTRY  \t\t", self.data["country"])
        print("\t[+] REGION   \t\t", self.data["regionName"])
        print("\t[+] TIME     \t\t", self.data["timezone"])
        print("\t[+] ZIP      \t\t", self.data["zip"])
        print("\t[+] LATITUDE \t\t", self.data["lat"])
        print("\t[+] LOMGITUDE\t\t", self.data["lon"])
    
    def __init__(self):
        self.get_domain()
        self.make_full_url()
        self.get_data()
        self.present_data()

if __name__ == "__main__":
    
    try:
        T = Tracer()
    except:
        print("\n[-] Please enter a valid Public IP or Domain.\n")
    
