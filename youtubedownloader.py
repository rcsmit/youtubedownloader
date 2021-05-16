
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 29 16:46:42 2019

@author: rcxsm

WORKS AGAIN. INFO BELOW JUST LEFT THERE FOR FUTURE REFERENCE

https://github.com/nficano/pytube/issues/591

-> install library
pip uninstall pytube
pip install pytube3
-> inside
NOPE  C:/Users/rcxsm/AppData/Local/Programs/Python/Python38/Lib/site-packages/pytube/pip/pytube/extract.py
C:/users/rcxsmi/Anaconda3/lib/site-packages/pytube/extract.py

-> find:
parse_qs(formats[i]["cipher"]) for i, data in enumerate(formats)
-> change it to
parse_qs(formats[i]["signatureCipher"]) for i, data in enumerate(formats)

https://stackoverflow.com/questions/64492922/pytube-only-works-periodically-keyerror-assets

https://stackoverflow.com/questions/63132116/too-many-values-to-unpack-in-pytube-module-problem
"""
import os
import os.path
import re
import time
import sys
from pytube import YouTube
from pytube import Playlist
from random import randint
from time import sleep



FFMPEGLOC = 'C://Users/rcxsm/Documents/phyton_scripts/'

def cleanup(test_string):
    """[summary]

    Args:
        test_string ([type]): [description]

    Returns:
        [type]: [description]
    """
    bad_chars = [":",';', ',', '/', ':', '!', "'","*","(",")"]
    result_string = ''.join(i for i in test_string if not i in bad_chars)
    #result_string = result_string.replace(" ", "_")
    return result_string

def download(durl):

    """[summary]
    """
    s1 = (int(time.time()))
     # Title and Time
    title=cleanup(((YouTube(durl)).title))
    _filename = (title)

    mp4 = "%s.mp4" % _filename
    mp3 = "%s.mp3" % _filename

    if os.path.isfile(mp3):
        print ("File exist already. I stop")
        sys.exit()

    print(f"Downloading.... {mp3}")
    #YouTube(durl).streams.first().download(filename=mp4)       # for video
    YouTube(durl).streams.get_audio_only().download(filename=mp3)     # for mp3

    s2 = (int(time.time()))
    s2x = s2-s1
    print("Downloading took " + str(s2x) + " seconds ....")

    # Converting - Not needed anymore since MP3's are downloaded directly
    # print("Converting... {_filename}")
    # os.chdir(FFMPEGLOC)
    # subprocess.call(['ffmpeg', '-i', mp4, mp3])

    s3 = (int(time.time()))
    s4 = s3-s1
    print ("\nCOMPLETE - Totaal aantal sec : "+ str(s4))

def countdown(t):
    """ Creating a countdown timer to show the wait time

    https://www.geeksforgeeks.org/how-to-create-a-countdown-timer-using-python/
    Args:
        t (integer): Wait time in seconds
    """    
    while t:
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        print(timer, end="\r")
        time.sleep(1)
        t -= 1



def downloadplaylist(url):
    #url = "https://www.youtube.com/watch?list=PLTo6svdhIL1cxS4ffGueFpVCF756ip-ab"
    YOUTUBE_STREAM_AUDIO = '140' # modify the value to download a different stream / mime_type="audio/mp4" abr="128kbps" acodec="mp4a.40.2"
    playlist = Playlist(url)

    # this fixes the empty playlist.videos list
    playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")

    # physically downloading the audio track
    for n,video in enumerate(playlist.videos):
        try:
            mp4 = video.title + ".mp4"
            if os.path.isfile(mp4):
                print (f"{n}/{len(playlist.video_urls)} | File {video.title}.mp4 exists already. ")
                no_wait = True
            else:


                print (f"Downloading {n}/{len(playlist.video_urls)} - {video.title}")
                audioStream = video.streams.get_by_itag(YOUTUBE_STREAM_AUDIO)
                audioStream.download()
                no_wait = False



        except:
            print (f"ERROR Downloading {n}/{len(playlist.video_urls)} ")
                    # some videos give 403 error
                    # too lazy to implement this (yet)
                    # https://github.com/pytube/pytube/issues/399
        if no_wait:
            pass
        else:
            wait_time = randint(10,30)
            print(f"Waiting {wait_time} seconds...")
            countdown(wait_time)
def main():
    url = input("URL: ")

    if "list" in url:
        downloadplaylist(url)
    else:
        download(url)

if __name__ == "__main__":
    main()
