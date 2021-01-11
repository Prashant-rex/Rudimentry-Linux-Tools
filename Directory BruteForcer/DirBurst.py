#!/usr/bin/env python3
import requests
import threading
import time

start = time.perf_counter()

class DirBust():


    def get_domain(self):    # function to prompt user for target domain.
        print("[+] Enter the target domain. ")
        self.target = input("[+]")
        return self.target

    def get_wordlist(self):  # get directory brute list from file.
        file = open("wordlist.txt")
        self.content = file.read()
        self.directory_list = self.content.splitlines() #split in lines to brute one by one.
        return self.directory_list
    
    def __init__(self):
        self.discovered_directory_paths = []  # list of discovered directory paths.
        self.directory_paths = self.get_wordlist()
        self.domain = self.get_domain()
        self.threads = []
    
    def find_directory_paths(self):
        for directory_path in self.directory_paths: # iterating over each directory path in directory_path list
            path = f"https://{self.domain}/{directory_path}"
            print("[+] Trying path : ", path)

            try:
                status = requests.get(path) # send get request to check if the path exists.
            except requests.ConnectionError: # if does not exist.
                pass # do nothing
            else:
                if (status.status_code == 404):
                    pass
                else:
                    print("[+] Discovered URL : ", path)
                    self.discovered_directory_paths.append(path) #append to list.

    def save_to_file(self): # function to save output list to file.
        with open("Discovered_Directory_paths.txt", "w") as outfile:
            for disovered_path in self.discovered_directory_paths:
                outfile.write(disovered_path + "\n")
            outfile.close()

if __name__ == "__main__":

    try:
        DB = DirBust()   

        DB.find_directory_paths()
        DB.save_to_file()

    except KeyboardInterrupt: #exit if keyboard interrupted. 
        print("[-] Keyboard interrupt Triggered. ")

finish = time.perf_counter()

print(f"[+] Finished in {round(finish-start, 2)} seconds. ")
