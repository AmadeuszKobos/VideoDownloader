import pytube.exceptions
from pytube import YouTube
from pathlib import Path
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk


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
        yt = YouTube(link, on_progress_callback=on_progress)

        video_title_label.configure(text="Title:\n" + yt.title, wraplength=300)
        video_title_label.pack(pady=10, padx=10)

        video_author_label.configure(text="Author:\n" + yt.author)
        video_author_label.pack(pady=10, padx=10)

        download_button.pack()
        progress_percentage.pack()
        progress_bar.pack(padx=10, pady=10)

    except pytube.exceptions.RegexMatchError as e:
        incorrect_url()
    except Exception as e:
        print("En error occured: ", e)


def download_video():
    try:
        link = entry.get()
        yt = YouTube(link, on_progress_callback=on_progress)
        stream = yt.streams.filter(res=resolution_combobox.get(), file_extension='mp4').first()
        path = Path('download_video').resolve()
        stream.download(path)
    except pytube.exceptions.RegexMatchError as e:
        incorrect_url()
    except Exception as e:
        print("En error occured in download: ", e)


def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_of_completion = bytes_downloaded / total_size * 100
    per = str(int(percentage_of_completion))
    progress_percentage.configure(text=per + '%')
    progress_percentage.update()

    progress_bar.set(float(percentage_of_completion / 100))


ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("400x300")
app.title("YT video downloader")

label = ctk.CTkLabel(app, text="Enter url address down below", wraplength=250)
label.pack()

search_frame = ctk.CTkFrame(master=app)
entry = ctk.CTkEntry(master=search_frame)
find_button = ctk.CTkButton(master=search_frame, text="Find", command=find_video)
entry.pack()
find_button.pack()
search_frame.pack()

video_author_label = ctk.CTkLabel(app)
video_title_label = ctk.CTkLabel(app)
resolution_combobox = ttk.Combobox(app)

download_button = ctk.CTkButton(app, text="Download", command=download_video)

progress_percentage = ctk.CTkLabel(app, text='0%')

progress_bar = ctk.CTkProgressBar(app, width=300)
progress_bar.set(0)

error_label = ctk.CTkLabel(app, text="Incorrect URL address", text_color='red')

app.mainloop()
