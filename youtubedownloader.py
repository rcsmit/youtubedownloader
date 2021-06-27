
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 29 16:46:42 2019

@author: rcxsm

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
import subprocess

import win32clipboard  # part of pywin32

def convert_to_mp3(mp4):
    if right(mp4,7) == "mp4.mp4":
        mp3 = left(mp4,(len(mp4)-7))+".mp3"
    else:
        mp3 = left(mp4,(len(mp4)-4))+".mp3"

    # Converting - Not needed anymore since MP3's are downloaded directly
    print(f"Converting... {mp4}")
    subprocess.call(['C:\\Users\\rcxsm\\Music\\MET PYTHON GEDOWNLOAD\\ffmpeg.exe', '-i', mp4, mp3])
    os.remove(mp4)


def cleanup(test_string):
    """Avoid forbidden characters in file names

    Args:
        test_string (string): the string to test

    Returns:
        result_string (string) : string without the bad characters
    """
    bad_chars = [":", ';', ',', '/', ':', '!', "'", "*", "(", ")"]
    result_string = ''.join(i for i in test_string if not i in bad_chars)
    #result_string = result_string.replace(" ", "_")
    return result_string

def left(s, amount):
    return s[:amount]
def right(s, amount):
    return s[-amount:]
def mid(s, offset, amount):
    return s[offset-1:offset+amount-1]

def countdown(t):
    """ Creating a countdown timer to show the wait time

        https://www.geeksforgeeks.org/how-to-create-a-countdown-timer-using-python/
    Args:
        t (integer): Wait time in seconds
    """
    while t:
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        print(f"Waiting : {timer}", end="\r")
        time.sleep(1)
        t -= 1


def download(durl, path_to_save, what):
    """ Download a file

    """
    s1 = (int(time.time()))
    # Title and Time
    # try:
    title = cleanup(((YouTube(durl)).title))
    # except:
    #    print ("Not a valid video URL and/or no video found")
    #    sys.exit()

    _filename = (title)


    mp4 = "%s.mp4" % _filename

    if os.path.isfile(mp4):
        print("File exist already. I stop")
        sys.exit()

    print(f"Downloading.... {_filename}")
    if what == "audio":
        #YouTube(durl).streams.first().download(filename=mp4)       # for music
        YouTube(durl).streams.get_by_itag(140).download(filename=mp4)
        new_filename = left(mp4,(len(mp4)-4))+"mp4.mp4" # for some reason files are saved as namemp4.mp4
        convert_to_mp3(new_filename)

    elif what == "video":
        YouTube(durl).streams.get_by_itag(18).download(filename=mp4)       # for video 360p

    s2 = (int(time.time()))
    s2x = s2-s1
    print("Downloading took " + str(s2x) + " seconds ....")

    s3 = (int(time.time()))
    s4 = s3-s1
    print("\nCOMPLETE - Totaal aantal sec : " + str(s4))

def downloadplaylist(url, path_to_save, what, ask, wait, START):
    """Downlaods the sound of the videos in a playlist
    Args:
        url (string): the URL with the word list in it
    """
    try:
        playlist = Playlist(url)
    except:
        print("Not a valid list URL and/or no list/videos found")
        sys.exit()

    # this fixes the empty playlist.videos list
    playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")
    STOP = 9990
                 #test purposes

    for n, video in enumerate(playlist.videos):
        if n >= START and n<STOP:
            try:
                mp4 = cleanup(video.title) + ".mp4"
                if ask:
                    dl_yes = input(
                        f"Download {n+1}/{len(playlist.video_urls)} - {video.title} ? (y/n/q) ")
                else:
                    dl_yes = "y"

                if dl_yes == "y" or dl_yes == "Y":
                    print(
                        f"Downloading {n+1}/{len(playlist.video_urls)} - {video.title}")

                    if what == "audio":
                        #video.streams.first().download(filename=mp4)       # for music
                        video.streams.get_by_itag(140).download(filename=mp4)
                        new_filename = path_to_save+left(mp4,(len(mp4)-4))+"mp4.mp4" # for some reason files are saved as namemp4.mp4
                        #convert_to_mp3(new_filename)

                    elif what == "video":
                        video.streams.get_by_itag(18).download(filename=mp4)       # for video 360p

                    if wait:
                        wait_time = randint(10, 30)
                        countdown(wait_time)


                elif dl_yes == "q" or dl_yes == "Q":
                    sys.exit()
            except SystemExit:
                print()
                print("Thank you for using this script.")
                sys.exit()
            except:
                print(
                    f"ERROR Downloading or finding the name of  {n+1}/{len(playlist.video_urls)} ")
                # some videos give 403 error
                # too lazy to implement this (yet)
                # https://github.com/pytube/pytube/issues/399

    main_convert(path_to_save)

def main_convert(path):
    s1 = (int(time.time()))
    number_of_files = 0
    with os.scandir(path) as it:
        for entry in it:
            if entry.name.endswith(".mp4") and entry.is_file():

                mp4 = str(entry.path)

                convert_to_mp3(mp4)
                number_of_files += 1

    print(f"COMPLETE - Totaal  {int(time.time() -s1)} sec. | {number_of_files} files => {round((time.time() -s1) / number_of_files)} sec. per file")



def main_download(path_to_save, what):
    current_path = os.getcwd()
    #os.chdir("C:\\Users\\rcxsm\\Music\\MET PYTHON GEDOWNLOAD\\")
    os.chdir(path_to_save)
    get_clipboard = True
    if get_clipboard:
        win32clipboard.OpenClipboard()
        url = win32clipboard.GetClipboardData()
        win32clipboard.CloseClipboard()
        if "youtube.com" in url:
            print(f"Retrieving {url}")
        else:
            url = input("URL to download: ")

    else:
        url = input("URL to download: ")

    if "list" in url:
        ask = True  # ask if you want to download each file
        wait =True  # wait a random number of seconds in between the downloads
        to_start_ = input("Where to start ? ")
        if to_start_ == None or to_start_=="":
            START = 0

        else:
            START = int(to_start_) - 1
        downloadplaylist(url,path_to_save, what, ask, wait, START)
    else:
        download(url, path_to_save, what)
    os.chdir(current_path)

def main():
    what = "audio"
    # DOWNLOAD AUDIO OR VIDEO FROM A URL OR LIST
    #main_download("C:\\Users\\rcxsm\\Music\\MET PYTHON GEDOWNLOAD\\nieuw\\", what)

    # BATCH CONVERT FILES IN A DIRECTORY FROM MP4 to MP3
    main_convert("C:\\Users\\rcxsm\\Music\\MET PYTHON GEDOWNLOAD\\nieuw\\toconvert\\")

    # CONVERT A SINGLE FILE
    # convert_to_mp3("C:\\Users\\rcxsm\\Music\\MET PYTHON GEDOWNLOAD\\nieuw\\Taylor Swift - Everything Has Changed ft Ed Sheeranmp4.mp4")

if __name__ == "__main__":
    main()

