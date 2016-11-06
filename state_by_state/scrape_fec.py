#!/bin/python2
import os
import urllib
import urllib2
import requests
from bs4 import BeautifulSoup
from getpass import getpass
import time
from ftplib import FTP
import sys

def download_file(url, dest):
    # NOTE the stream=True parameter
    r = requests.get(url.strip(), stream=True)
    with open(dest, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                #f.flush() commented by recommendation from J.F.Sebastian

site = "http://www.fec.gov/disclosurep/PDownload.do"
r = requests.get(site)

soup = BeautifulSoup(r.content)
states = soup.find_all("td", {"class": "table-content-center"})

for i, tag in enumerate(states):
    if i == 0 or i == 1 or i == 2:
        continue
    a = tag.find("a")
    link = a.attrs['href'].strip()
    dest = link.split('/')[-1]

    print(repr(link))
    #urllib.urlretrieve(link, dest)

    ftp = FTP(link)

    ftp.retrbinary("RETR" + link, open(dest, 'wb').write)
    #except:
    #    print("ERROR")

#    time.sleep(1)
    #r = requests.get(link)
    #with open(dest, 'wb') as f:
    #    f.write(r.content)
    #download_file(link, dest)
    #sys.exit()
