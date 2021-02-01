# -*- coding: utf-8 -*-
import os
import pyperclip as pc
import subprocess
# from pytube import YouTube
import pytube
from http.client import RemoteDisconnected
from socket import gaierror
from urllib.error import URLError

musicfolder = r'C:\Users\jorda\Downloads\music'
videofolder = r'C:\Users\jorda\Downloads\videos'

banner = '''
 ▄· ▄▌      ▄• ▄▌▄▄▄▄▄▄• ▄▌▄▄▄▄· ▄▄▄ .    ·▄▄▄▄        ▄▄▌ ▐ ▄▌ ▐ ▄ ▄▄▌         ▄▄▄· ·▄▄▄▄  ▄▄▄ .▄▄▄  
▐█▪██▌▪     █▪██▌•██  █▪██▌▐█ ▀█▪▀▄.▀·    ██▪ ██ ▪     ██· █▌▐█•█▌▐███•  ▪     ▐█ ▀█ ██▪ ██ ▀▄.▀·▀▄ █·
▐█▌▐█▪ ▄█▀▄ █▌▐█▌ ▐█.▪█▌▐█▌▐█▀▀█▄▐▀▀▪▄    ▐█· ▐█▌ ▄█▀▄ ██▪▐█▐▐▌▐█▐▐▌██▪   ▄█▀▄ ▄█▀▀█ ▐█· ▐█▌▐▀▀▪▄▐▀▀▄ 
 ▐█▀·.▐█▌.▐▌▐█▄█▌ ▐█▌·▐█▄█▌██▄▪▐█▐█▄▄▌    ██. ██ ▐█▌.▐▌▐█▌██▐█▌██▐█▌▐█▌▐▌▐█▌.▐▌▐█ ▪▐▌██. ██ ▐█▄▄▌▐█•█▌
  ▀ •  ▀█▄▀▪ ▀▀▀  ▀▀▀  ▀▀▀ ·▀▀▀▀  ▀▀▀     ▀▀▀▀▀•  ▀█▄▀▪ ▀▀▀▀ ▀▪▀▀ █▪.▀▀▀  ▀█▄▀▪ ▀  ▀ ▀▀▀▀▀•  ▀▀▀ .▀  ▀


'''
downloadindicator='''
\t░░░░░░░░░░░║
\t░░▄█▀▄░░░░░║░░░░░░▄▀▄▄
\t░░░░░░▀▄░░░║░░░░▄▀
\t░▄▄▄░░░░█▄▄▄▄▄▄█░░░░▄▄▄
\t▀░░░▀█░█▀░░▐▌░░▀█░█▀░░░▀
\t░░░░░░██░░▀▐▌▀░░██
\t░▄█▀▀▀████████████▀▀▀█
\t█░░░░░░██████████░░░░░▀▄
\t█▄░░░█▀░░▀▀▀▀▀▀░░▀█░░░▄█
\t░▀█░░░█░░░░░░░░░░█░░░█▀
'''
def getvideofromurl(url):
    print("####  Getting Video from url: {0}".format(url))
    video = pytube.YouTube(url,on_progress_callback=progressBar)
    #print("#### {0}".format(video.title))
    return video

def viewstreamsfordownload(streams,title,mp3=True):
    bitrates = {}
    for s in streams.filter(only_audio=True):
        bitrates[int(s.abr.strip('kbps'))] = s
    # print("####  Bitrates: ",list(bitrates.keys()))
    fastest = max(list(bitrates.keys()))
    if mp3:
        return bitrates[fastest]
    resolutions = ['1080p','720p','480p','360p','240p','144p']
    for r in resolutions:
        objs = streams.filter(only_video=True,res=r)
        if objs==None:
            continue
        else:
            return bitrates[fastest],objs[0]

def savemp3(stream,title):
    os.chdir(musicfolder)
    print(downloadindicator)
    print("\t"+title.replace('"',''))
    stream.download(filename='temp')
    destination = title+'.mp3'
    destination = destination.replace('"','')
    FNULL = open(os.devnull, 'w')
    ffmpeg = 'ffmpeg -i {0} -vn -ab 128k -ar 44100 -y "{1}"'.format('temp.webm',destination)
    subprocess.run(ffmpeg,stdout=FNULL,stderr=subprocess.STDOUT)
    os.remove('temp.webm')


def savevideo(audiostream,videostream,title):
    os.chdir(videofolder)
    print(downloadindicator)
    print("\t"+title.replace('"',''))
    audiostream.download(filename='temp')
    videostream.download(filename='temp')
    title = title.replace('"','')
    command = 'ffmpeg -i {0} -i {1} -acodec copy -vcodec copy "{2}"'.format('temp.webm','temp.mp4',title+'.mp4')
    FNULL = open(os.devnull, 'w')
    #progress bar
    subprocess.run(command,stdout=FNULL,stderr=subprocess.STDOUT)
    os.remove('temp.webm')
    os.remove('temp.mp4')

def progressBar(stream,chunk,bytes_remaining):
    totalSize = stream.filesize
    downloaded = totalSize - bytes_remaining
    percent = "{0:.1f}".format(100*downloaded/float(totalSize))
    fillLength = int(50*downloaded//totalSize)
    bar = '█'*fillLength+'-'*(50-fillLength)
    print(f'Downloading: |{bar}| {percent}% Complete',end='\r')
    if totalSize==downloaded:
        print()

def getdownloadoption(title):
    while True:
        print("####  Select your download option for: {0}".format(title))
        print("####  (a) AUDIO\t(v) VIDEO")
        print("####  Enter: ",end='')
        while True:
            opt = input().upper()
            if opt=='A' or opt=='V':
                break
            print("####  Enter 'a' for audio OR 'v' for video: ",end='')
        return opt

def menu():
    while True:
        #print("\n\n@#$&  ::WELCOME YO YOUR YOUTUBE DOWNLOADER::\n")
        print("####  (a) PASTE LINK\t(q) EXIT")
        print("####  Enter: ",end='')
        while True:
            choice = input().upper()
            if choice=='A' or choice=='Q':
                break
            print("####  Enter 'a' to paste a link or 'q' to close the program: ",end='')
        if choice=='A':
            url = pc.paste()
            while True:
                try:
                    video = getvideofromurl(url)
                    break
                except pytube.exceptions.RegexMatchError:
                    print("####  The link provided was not valid.\n####  Please paste a valid link here: ",end='')
                    url = input()
                except (RemoteDisconnected,gaierror,URLError,ConnectionResetError):
                    print("####  There was a network error while attempting to fetch video data. Try again later.")
                    exit(1)
        
            opt = getdownloadoption(video.title)
            if opt=='A':
                stream = viewstreamsfordownload(video.streams,video.title,mp3=(opt=='A'))              
                savemp3(stream,video.title)
            else:
                audio_stream,video_stream = viewstreamsfordownload(video.streams,video.title,mp3=(opt=='A'))
                savevideo(audio_stream,video_stream,video.title)
        elif choice=='Q':
            print("\n\t\tExitting. Good-bye!")
            break

def main():
    os.system('cls')
    print(banner)
    menu()

if __name__=='__main__':
    main()