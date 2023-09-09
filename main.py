import pytube.exceptions
from pytube import YouTube
from pathlib import Path
import customtkinter as ctk


class DownloaderAppGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        # window settings
        self.title("YT video downloader")
        self.geometry("400x300")

        # Variable for options menu
        self.file_type_var = ctk.StringVar(value="MP3")

        # Options menu settings
        self.options_menu = ctk.CTkOptionMenu(master=self, values=["MP3", "MP4"], variable=self.file_type_var)
        self.options_menu.pack()

        # Entry label settings
        self.label = ctk.CTkLabel(self, text="Enter url address down below", wraplength=250)
        self.label.pack()

        # Frame for URL entry
        self.search_frame = ctk.CTkFrame(master=self)

        # URL entry settings
        self.entry = ctk.CTkEntry(master=self.search_frame)
        self.entry.pack()

        # Find button for URL entry
        self.find_button = ctk.CTkButton(master=self.search_frame, text="Find", command=self.find_video)
        self.find_button.pack()

        # Pack frame with all elements
        self.search_frame.pack()

        # Search result
        # Video Author
        self.video_author_label = ctk.CTkLabel(self)

        # Video Title
        self.video_title_label = ctk.CTkLabel(self)

        # Download button displayed after a successful search
        self.download_button = ctk.CTkButton(self, text="Download", command=self.download_video, state=ctk.NORMAL)

        # Display information about current percentage of download
        self.progress_percentage_label = ctk.CTkLabel(self, text='0%')

        self.progress_bar = ctk.CTkProgressBar(self, width=300)
        self.progress_bar.set(0)

        self.download_package_label = ctk.CTkLabel(self, font=("Arial", 15), text='0')

        # Display info about wrong URL address
        self.error_label = ctk.CTkLabel(self, text="Incorrect URL address", text_color='red')

    def incorrect_url(self):
        self.error_label.pack()
        if self.download_button.winfo_ismapped():
            self.download_button.pack_forget()

    def find_video(self):
        try:
            if self.error_label.winfo_ismapped():
                self.error_label.pack_forget()

            link = self.entry.get()
            yt = YouTube(link)

            self.video_title_label.configure(text=f"Title:\n{yt.title}", wraplength=300)
            self.video_title_label.pack(pady=10, padx=10)

            self.video_author_label.configure(text=f"Author:\n{yt.author}")
            self.video_author_label.pack(pady=10, padx=10)

            self.download_button.pack()
            self.progress_percentage_label.configure(text='0%')
            self.progress_percentage_label.pack()

            self.progress_bar.set(0)
            self.progress_bar.pack(padx=10, pady=10)

        except pytube.exceptions.RegexMatchError as e:
            self.incorrect_url()
        except Exception as e:
            print(f"En error occurred: {e}")

    def download_video(self):
        try:
            self.download_button.configure(state=ctk.DISABLED)
            self.download_package_label.pack()

            link = self.entry.get()
            yt = YouTube(link, on_progress_callback=self.on_progress)
            stream = yt.streams.get_lowest_resolution()
            path = str(Path('download_video').resolve())
            stream.download(output_path=path, filename=f"{yt.title}.mp3", skip_existing=False)

            # After download
            if self.download_button.winfo_ismapped():
                self.download_button.pack_forget()

        except pytube.exceptions.RegexMatchError as e:
            self.incorrect_url()
        except Exception as e:
            print(f"En error occurred in download: {e}")

    def on_progress(self, stream, chunk, bytes_remaining):
        total_size = stream.filesize  # get size of file we are currently downloading
        bytes_downloaded = total_size - bytes_remaining  # check number of bytes already downloaded
        percentage_of_completion = bytes_downloaded / total_size * 100  # calculate percentage of progress
        per = str(round(percentage_of_completion, 2))  # conversion to int, then to string in order to write out
        self.progress_percentage_label.configure(text=per + '%')  # add '%' to our percentage number
        self.progress_percentage_label.update()  # update progress widget
        self.progress_bar.set(float(percentage_of_completion / 100))  # setting the current progress of download

        mb_downloaded = round(bytes_downloaded / 1048576, 2)  # converting bytes to megabytes
        mb_total = round(total_size / 1048576, 2)

        self.download_package_label.configure(
            text=f"{str(mb_downloaded)}MB / {mb_total}MB")  # setting the current download status
        self.download_package_label.update()


if __name__ == "__main__":
    app = DownloaderAppGUI()
    app.mainloop()
