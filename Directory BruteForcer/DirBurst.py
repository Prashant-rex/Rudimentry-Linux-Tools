#!/usr/bin/env python3
import requests
import threading
import time

start = time.perf_counter()

def get_domain():    # function to prompt user for target domain.
    print("[+] Enter the target domain. ")
    target = input("[+]")
    return target

def get_wordlist():  # get directory brute list from file.
    file = open("wordlist.txt")
    content = file.read()
    directory_list = content.splitlines() #split in lines to brute one by one.
    return directory_list

discovered_directory_paths = [] # list of discovered directory paths.
def find_directory_paths():

    directory_paths = get_wordlist()
    domain = get_domain()

    for directory_path in directory_paths: # iterating over each directory path in directory_path list
        path = f"https://{domain}/{directory_path}"

        try:
            requests.get(path) # send get request to check if the path exists.
        except requests.ConnectionError: # if does not exist.
            pass # do nothing
        else:
            print("[+] Discovered URL : ", path)
            discovered_directory_paths.append(path) #append to list.

def save_to_file(): # function to save output list to file.
    with open("Discovered_Directory_paths.txt", "w") as outfile:
        for disovered_path in discovered_directory_paths:
            outfile.write(disovered_path)
        outfile.close()

print("[+] How many threads you want to use? ")
thread_count = input("[+] ")
if (thread_count < 0 or thread_count > 200):
    print("[+] Please Enter threads in the range of 1 to 200.")
    exit()
    
threads = []

for _ in range(thread_count):
    t = threading.Thread(target = find_directory_paths())
    t.start()
    threads.append(t)

for thread in threads:
    thread.join()

find_directory_paths()
save_to_file()
if KeyboardInterrupt: # exit if Keyboard Interrupt.
    print("[-] Keyboard innterupt Triggered. ")

finish = time.perf_counter()

print(f"[+] Finished in {round(finish-start, 2)} seconds. ")
