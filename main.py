import pytube.exceptions
from pytube import YouTube
from pathlib import Path
import tkinter as tk
from tkinter import ttk


def incorrect_url():
    error_label.pack()
    if download_button.winfo_ismapped():
        download_button.pack_forget()


def get_resolutions():
    link = entry.get()
    try:
        yt = YouTube(link)
        resolutions = yt.streams.filter(file_extension="mp4").order_by("resolution").desc()
        res_available = [str(stream.resolution) for stream in resolutions]
        resolution_combobox["values"] = res_available
        default_res = res_available[-1]
        resolution_combobox.set(default_res)
    except Exception as e:
        resolution_combobox["values"] = []


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

        get_resolutions()
        resolution_combobox.pack()

        download_button.pack()

    except pytube.exceptions.RegexMatchError as e:
        incorrect_url()
    except Exception as e:
        print("En error occured: ", e)


def download_video():
    try:
        link = entry.get()
        yt = YouTube(link)
        stream = yt.streams.filter(res=resolution_combobox.get(), file_extension='mp4').first()
        path = Path('download_video').resolve()
        stream.download(path)

    except pytube.exceptions.RegexMatchError as e:
        incorrect_url()
    except Exception as e:
        print("En error occured in download: ", e)


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
resolution_combobox = ttk.Combobox(app)

download_button = tk.Button(app, text="Download", command=download_video)

error_label = tk.Label(app, text="Incorrect URL address", fg="red")

app.mainloop()
