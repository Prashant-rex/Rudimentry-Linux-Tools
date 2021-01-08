#!/usr/bin/env python
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

    
if __name__ == "__main__":

    print("[+] Enter the absolute link to file.")
    file_to_get = input("[+] ")
    D = Downloader()
    D.download(file_to_get)
    print("[+] Downloading file.......")
    print("[+] Downloaded file as " + D.get_file_name(file_to_get))


