#-*- coding: utf-8 -*-
__author__ = "Chirag Rathod (Srce Cde)"
__license__ = "GPL 3.0"
__email__ = "chiragr83@gmail.com"
__maintainer__ = "Chirag Rathod (Srce Cde)"

import os
import sys
import argparse
from urllib.parse import urlparse, urlencode, parse_qs
from youtube.videos_channelid import channelVideo
from youtube.search_keyword import searchVideo
from youtube.video_comments import VideoComment
from __future__ import unicode_literals
import youtube_dl
from config import SAVE_PATH

def main():
    os.makedirs("output", exist_ok=True)
    parser = argparse.ArgumentParser()

    if str(sys.argv[1]) == "--s":
        
        parser.add_argument("--s", help="calls the search by keyword function", action='store_true')
        parser.add_argument("--r", help="define country code for search results for specific country", default="IN")
        parser.add_argument("--search", help="Search Term", default="Srce Cde")
        parser.add_argument("--max", help="number of results to return", default=10)
        parser.add_argument("--key", help="Required API key", required=True)
        args = parser.parse_args()

        sv = searchVideo(args.search, args.max, args.r, args.key)
        sv.get_channel_videos()

    elif str(sys.argv[1]) == "--sc":
        parser.add_argument("--sc", help="calls the search by channel by keyword function", action='store_true')
        parser.add_argument("--channelid", help="channel id", required=True)
        parser.add_argument("--max", help="number of results to return", default=10)
        parser.add_argument("--key", help="Required API key", required=True)
        args = parser.parse_args()

        cv = channelVideo(args.channelid, args.max, args.key)
        cv.get_channel_videos()

    elif str(sys.argv[1]) == "--c":
        parser.add_argument("--c", help="calls comment function by keyword function", action='store_true')
        parser.add_argument("--max", help="number of comments to return", default=10)
        parser.add_argument("--videourl", help="Required URL for which comments to return", required=True)
        parser.add_argument("--key", help="Required API key", required=True)
        args = parser.parse_args()
        video_id = urlparse(str(args.videourl))
        q = parse_qs(video_id.query)
        vid = q["v"][0]

        vc = VideoComment(args.max, vid, args.key)
        vc.get_video_comments()

     elif str(sys.argv[1]) == "--cl":
        parser.add_argument("--cl", help="get video urls from playlist and calls comment function by keyword function", action='store_true')
        parser.add_argument("--max", help="number of comments to return", default=10)
        parser.add_argument("--listurl", help="Required URL for which comments to return", required=True)
        parser.add_argument("--key", help="Required API key", required=True)
        args = parser.parse_args()
        
        listurl = str(args.listurl)
        download = False 
        ydl_opts = {
            'outtmpl': SAVE_PATH+"videosInList.csv",     // output filename
            'writesubtitles': True,
            'format': 'mp4',
            'writethumbnail': True
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ie_result = ydl.extract_info(url, download)
            
        for item in ie_result:
            video_id = urlparse(str(args.videourl))
            q = parse_qs(video_id.query)
            vid = q["v"][0]

            vc = VideoComment(args.max, vid, args.key)
            vc.get_video_comments()

    else:
        print("Invalid Arguments\nAdd --s for searching video by keyword after the filename\nAdd --sc to list vidoes based on channel id")

if __name__ == '__main__':
    main()
