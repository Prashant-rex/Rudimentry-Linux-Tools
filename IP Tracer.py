#!/usr/bin/env/python

import requests
import json

print("[+] Enter the IP Address or name of Website you want to know details of.")
ip = input("[+] ")
print("")

url = "http://ip-api.com/json/" + ip  #combining the provided ip with api to form the full url.

#http://ip-api/json/192.168.0.1

response = requests.get(url) #sending get request to the url.
data = json.loads(response.content)  #getting the content of the json file.
    
print("\t[+] IP       \t\t", data["query"])
print("\t[+] CITY     \t\t", data["city"])
print("\t[+] ISP      \t\t", data["isp"])
print("\t[+] COUNTRY  \t\t", data["country"])
print("\t[+] REGION   \t\t", data["regionName"])
print("\t[+] TIME     \t\t", data["timezone"])
print("\t[+] ZIP      \t\t", data["zip"])
print("\t[+] LATITUDE \t\t", data["lat"])
print("\t[+] LOMGITUDE\t\t", data["lon"])