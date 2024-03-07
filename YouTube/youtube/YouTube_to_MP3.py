import os
import sys
from pytube import YouTube


def download_audio(video_url):
    try:
        yt = YouTube(video_url)
        audio_stream = yt.streams.get_audio_only()
        output_file = audio_stream.download()
        # Renaming the file to have a .mp3 extension
        base, ext = os.path.splitext(output_file)
        new_file = base + '.mp3'
        os.rename(output_file, new_file)
        print(f"Downloaded audio '{yt.title}.mp3' successfully.")
    except Exception as e:
        print(f"Failed to download audio: {e}")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python YouTube_to_MP3.py 'url'")
        sys.exit(1)
    video_url = sys.argv[1]
    download_audio(video_url)
