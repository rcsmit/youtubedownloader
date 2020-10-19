
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 29 16:46:42 2019

@author: rcxsm

This script is downloading the video (.mp4) first and will convert it into an audio file (.mp3)
If there is 'list'in the URL, it will download the comlete list


Place ffmpeg.exe in the directory stated in the beginning of the script. 
Download it at https://ffmpeg.org/


WHEN HAVING A PROBLEM READ THIS https://github.com/nficano/pytube/issues/591

-> install library
pip uninstall pytube
pip install pytube3
-> inside


pip/pytube/extract.py

in my case C:/Users/heyitsme/AppData/Local/Programs/Python/Python38/Lib/site-packages/pytube


-> find:
parse_qs(formats[i]["cipher"]) for i, data in enumerate(formats)
-> change it to
parse_qs(formats[i]["signatureCipher"]) for i, data in enumerate(formats)


"""

from pytube import YouTube
import os
import subprocess
import time
import os.path
import sys
from pytube import Playlist
    

ffmpegloc = 'C://Users/heyitsme/Documents/phyton_scripts/'
    
    
def cleanup(test_string):   
    bad_chars = [":",';', ',', '/', ':', '!', "'","*","(",")"] 
    result_string = ''.join(i for i in test_string if not i in bad_chars) 
    result_string = result_string.replace(" ", "_")  
    return result_string
    
def download(durl):
    s1 = (int(time.time()))
     # Title and Time
    print("...")
    print(((YouTube(durl)).title))
    print (durl)
    print("...")
    title=cleanup(((YouTube(durl)).title))
    
    # Filename specification
    _filename = (title)
    
    mp4 = "%s.mp4" % _filename
    mp3 = "%s.mp3" % _filename
    
    if os.path.isfile(mp4):
        print ("File exist already. I stop")
        sys.exit()
    else:
        print ("File doesn't exist, let's continue")
   
    # Downloading
    print("Downloading....")
    YouTube(durl).streams.first().download(filename=_filename)
    
    s2 = (int(time.time()))
    s2x = s2-s1
    print("Downloading took " + str(s2x) + " seconds ....")
    # Converting
    print("Converting....")
  
    os.chdir(ffmpegloc)
    subprocess.call(['ffmpeg', '-i', mp4, mp3])
    
    s3 = (int(time.time()))
    s4 = s3-s1
    print ("\nCOMPLETE - Totaal aantal sec : "+ str(s4))

def downloadplaylist(url):
    pl = Playlist(url)
    n=1
    pl.populate_video_urls()  # fills the pl.video_urls with all links from the playlist
    urls = pl.video_urls
    lengte = (len(pl.video_urls))
    for xurl in urls:
        print ("------------------------------------------")
        print ( str(n) + " out of " + str(lengte))
        download (xurl)
        n=n+1
  
def main():
    url = input("URL: ")
    
    if "list" in url:
        downloadplaylist(url)
    else:
        download(url)
    
main()
