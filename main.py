import pytube.exceptions
from pytube import YouTube
from sys import argv, exit
from pathlib import Path
import tkinter as tk


def incorrect_url():
    error_label.pack()
    if download_button.winfo_ismapped():
        download_button.pack_forget()

def find_video():
    try:
        if error_label.winfo_ismapped():
            error_label.pack_forget()

        link = entry.get()
        yt = YouTube(link)

        video_title_label.config(text="Title:\n" + yt.title)
        video_title_label.pack()

        video_author_label.config(text="Author:\n" + yt.author)
        video_author_label.pack()

        download_button.pack()

    except pytube.exceptions.RegexMatchError as e:
        incorrect_url()
    except Exception as e:
        print("En error occured: ", e)

def download_video():
    try:
        link = entry.get()
        yt = YouTube(link)
        stream = yt.streams.get_lowest_resolution()
        path = Path('download_video').resolve()
        stream.download(path)

    except pytube.exceptions.RegexMatchError as e:
        incorrect_url()
    except Exception as e:
        print("En error occured: ", e)


app = tk.Tk()
app.title("YT video downloader")
app.geometry("400x300")


label = tk.Label(app, text="Enter url address down below", wraplength=250)
label.pack()

entry = tk.Entry(app)
entry.pack()

find_button = tk.Button(app, text="Find", command=find_video)
find_button.pack()

video_author_label = tk.Label(app)
video_title_label = tk.Label(app)

download_button = tk.Button(app, text="Download", command=download_video)

error_label = tk.Label(app, text="Incorrect URL address", fg="red")

app.mainloop()

# if __name__ == "__main__":
#     if len(argv) != 2:
#         print("Invalid arguments", len(argv))
#         exit(1)
#     else:
#         download_video(argv[1])
