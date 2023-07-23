import pytube.exceptions
from pytube import YouTube
from sys import argv, exit
from pathlib import Path
import tkinter as tk


def incorrect_url():
    error_label.pack()


def download_video():
    try:
        if error_label.winfo_ismapped():
            error_label.pack_forget()

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

label = tk.Label(app, text="Enter url address down below")
label.pack()

entry = tk.Entry(app)
entry.pack()

button = tk.Button(app, text="Download", command=download_video)
button.pack()

error_label = tk.Label(app, text="Incorrect URL address", fg="red")

app.mainloop()

# if __name__ == "__main__":
#     if len(argv) != 2:
#         print("Invalid arguments", len(argv))
#         exit(1)
#     else:
#         download_video(argv[1])
