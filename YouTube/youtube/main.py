
import sys
from pytube import YouTube


def download_video(video_url):
    try:
        yt = YouTube(video_url)
        stream = yt.streams.get_highest_resolution()
        stream.download()
        print(f"Downloaded '{yt.title}' successfully.")
    except Exception as e:
        print(f"Failed to download video: {e}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        video_url = sys.argv[1]
        download_video(video_url)
    else:
        print("Please provide a YouTube video URL as an argument.")
