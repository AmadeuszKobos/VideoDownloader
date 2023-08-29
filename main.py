import pytube.exceptions
from pytube import YouTube
from pathlib import Path
import customtkinter as ctk
import os


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

        video_title_label.configure(text=f"Title:\n{yt.title}", wraplength=300)
        video_title_label.pack(pady=10, padx=10)

        video_author_label.configure(text=f"Author:\n{yt.author}")
        video_author_label.pack(pady=10, padx=10)

        download_button.pack()
        progress_percentage_label.pack()
        progress_bar.pack(padx=10, pady=10)
        download_package_label.pack()

    except pytube.exceptions.RegexMatchError as e:
        incorrect_url()
    except Exception as e:
        print(f"En error occurred: {e}")


def download_video():
    try:
        link = entry.get()
        yt = YouTube(link, on_progress_callback=on_progress)
        stream = yt.streams.get_lowest_resolution()
        path = str(Path('download_video').resolve())
        stream.download(output_path=path, filename=f"{yt.title}.mp3", skip_existing=False)
    except pytube.exceptions.RegexMatchError as e:
        incorrect_url()
    except Exception as e:
        print(f"En error occurred in download: {e}")


def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize                                    # get size of file we are currently downloading
    bytes_downloaded = total_size - bytes_remaining                 # check number of bytes already downloaded
    percentage_of_completion = bytes_downloaded / total_size * 100  # calculate percentage of progress
    per = str(round(percentage_of_completion, 2))                   # conversion to int, then to string in order to write out
    progress_percentage_label.configure(text=per + '%')             # add '%' to our percentage number
    progress_percentage_label.update()                              # update progress widget
    progress_bar.set(float(percentage_of_completion / 100))         # setting the current progress of download

    mb_downloaded = round(bytes_downloaded / 1048576, 3)            # converting bytes to megabytes
    mb_total = round(total_size / 1048576, 3)

    download_package_label.configure(text=f"{str(mb_downloaded)}MB / {mb_total}MB")     # setting the current download status
    download_package_label.update()


if __name__ == "__main__":
    # setting app style
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    # setting app window
    app = ctk.CTk()
    app.geometry("400x300")
    app.title("YT video downloader")

    # Entry label
    label = ctk.CTkLabel(app, text="Enter url address down below", wraplength=250)
    label.pack()

    # Frame for URL entry + 'Find' button
    search_frame = ctk.CTkFrame(master=app)
    entry = ctk.CTkEntry(master=search_frame)
    entry.pack()
    find_button = ctk.CTkButton(master=search_frame, text="Find", command=find_video)
    find_button.pack()
    search_frame.pack()
    # End of search frame and elements in this frame declaration

    # Display information about the found video
    video_author_label = ctk.CTkLabel(app)
    video_title_label = ctk.CTkLabel(app)

    # Download button displayed after a successful search
    download_button = ctk.CTkButton(app, text="Download", command=download_video)

    # Display information about current percentage of download
    progress_percentage_label = ctk.CTkLabel(app, text='0%')
    progress_bar = ctk.CTkProgressBar(app, width=300)
    progress_bar.set(0)
    download_package_label = ctk.CTkLabel(app, font=("Arial", 15), text='0')

    # Display info about wrong URL address
    error_label = ctk.CTkLabel(app, text="Incorrect URL address", text_color='red')

    app.mainloop()
