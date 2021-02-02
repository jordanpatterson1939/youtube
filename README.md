# YTDL

Simple command line tool for downloading audio from YouTube. Can also download videos. Requires ffmpeg to already be installed.


**Download**

> git clone https://github.com/jordanpatterson1939/ytdl.git

> setup.py install

> Edit config.json and insert the location where you want your audio and video files to go.   

```json
    {
        "musicfolder" : "path/to/save/audio/files/goes/here",
        "videofolder" : "path/to/save/video/files/goes/here"
    }
```

# Todo:
* Add option to set filename after downloading.
* Command line argument parsing capabilities.
* Add option to paste different link
