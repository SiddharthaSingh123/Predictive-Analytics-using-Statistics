import yt_dlp
import os

def download_videos(singer, n, base_dir):

    download_path = os.path.join(base_dir, "downloads")

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': download_path + '/%(title)s.%(ext)s',
        'noplaylist': True,
        'quiet': True
    }

    search_query = f"ytsearch{n}:{singer} songs"

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([search_query])
