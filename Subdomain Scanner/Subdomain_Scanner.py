#!/usr/bin/env python3
import requests
import threading

def get_domain():    # function to prompt user for target domain.
    print("[+] Enter the target domain. ")
    target = input("[+]")
    return target

def get_subdomain_list():  # get subdomain brute list from file.
    file = open("subdomain_wordlist.txt")
    content = file.read()
    subdomains_list = content.splitlines() #split in lines to brute one by one.
    return subdomains_list


discovered_subdomains = [] # list of discovered subdomains.
def find_subdomains():

    subdomains = get_subdomain_list()
    domain = get_domain()

    for subdomain in subdomains: # iterating over each subdomain in subdomain list
        https_url = f"https://{subdomain}.{domain}"

        try:
            requests.get(https_url) # send get request to check if the site exists.
        except requests.ConnectionError: # if does not exist.
            pass # do nothing
        else:
            print("[+] Discovered Subdomain : ", https_url)
            discovered_subdomains.append(https_url) #append to list.

def save_to_file(): # function to save output list to file.
    with open("Discovered_subdomains.txt", "w") as outfile:
        for subdomain in discovered_subdomains:
            outfile.write(subdomain)
        outfile.close()

print("[+] How many threads you want to use? ")
thread_count = int(input("[+] "))
if (thread_count < 0 or thread_count > 200):
    print("[+] Please Enter threads in the range of 1 to 200.")
    exit()

threads = []

for _ in range(thread_count):
    t = threading.Thread(target = find_subdomains)
    t.start()
    threads.append(t)

for thread in threads:
    thread.join()

    
find_subdomains()
save_to_file()
if KeyboardInterrupt: # exit if Keyboard Interrupt.
    print("[-] Keyboard innterupt Triggered. ")
