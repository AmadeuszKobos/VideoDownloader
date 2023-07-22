from pytube import YouTube
from sys import argv, exit
from pathlib import Path

def download_video(link):
    try:
        yt = YouTube(link)
        stream = yt.streams.get_lowest_resolution()
        path = Path('download_video').resolve()
        stream.download(path)
    except Exception as e:
        print("En error occured")
        exit(1)

def create_folder():
    try:
        Path('downloaded_video').mkdir()
        folder_path = Path('downloaded_video').resolve()
        print("Created folder for downloaded videos.\n", folder_path)
    except:
        print("En error occured")
        exit(1)
if __name__ == "__main__":
    if len(argv) != 2:
        print("Invalid arguments", len(argv))
        exit(1)
    else:
        download_video(argv[1])
