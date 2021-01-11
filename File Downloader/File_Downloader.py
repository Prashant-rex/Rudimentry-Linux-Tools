#!/usr/bin/env python3
import requests  #importing the requests library

class Downloader:
    def get_file_name(self, url): #function to get file name.
        self.url = url
        file_name = url.split("/")[-1] #splitting and getting the last element from the url i.e the file name to download
        return file_name

    def download(self, url):  # download fucntion to actually get the file
        self.url = url
        get_response = requests.get(self.url) # sending get request to the url
        file_name = self.get_file_name(self.url) 
    
        with open(file_name, "wb") as out_file: #creating a file name with the same name as original with extension and openning it for write as binary.
            out_file.write(get_response.content) # writng the contents of the get requests to the file created.

    def get_link(self): # function to get the link from the user.
        print("[+] Enter the absolute link to file.")
        self.file_to_get = input("[+] ")
        return self.file_to_get
    
    def complete_prompt(self): # funtion to prompt the download complete.
        print("[+] Downloading file.......")
        print("[+] Downloaded file as " + self.get_file_name(self.file_to_get))
    
if __name__ == "__main__":
  
    try:
        D = Downloader()
    
        link = D.get_link()
        D.download(link)
        D.complete_prompt()
    
    except requests.exceptions.MissingSchema:  # handling if user input provided is is not a VALID URL.
        print("[-] Please provide a valid URL.")
    except requests.exceptions.ConnectionError: # handling if the file does not exist
        print("[-] File not found.")


