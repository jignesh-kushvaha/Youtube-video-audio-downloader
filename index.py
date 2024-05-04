import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from pytube import YouTube
import os

class YouTubeDownloaderApp:
    def __init__(self, master):
        self.master = master
        self.master.title("YouTube Downloader")
        self.master.geometry("500x500+400+100")
        self.master.resizable(False, False)
        self.create_widgets()

    def create_widgets(self):
        
        self.label_url = tk.Label(self.master, text="Enter YouTube URL:",font=("Arial",10))
        self.label_url.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.entry_url = tk.Entry(self.master, width=40)
        self.entry_url.grid(row=0, column=1, padx=10, pady=10)

        self.label_type = tk.Label(self.master, text="Select Download Type:",font=("Arial",10))
        self.label_type.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.var_type = tk.StringVar(value="video")
        self.radio_video = tk.Radiobutton(self.master, text="Video", variable=self.var_type, value="video",cursor="hand2",font=("Roboto",10), command=self.toggle_resolution_dropdown)
        self.radio_video.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        self.radio_audio = tk.Radiobutton(self.master, text="Audio", variable=self.var_type, value="audio", cursor="hand2",font=("Arial",10), command=self.toggle_resolution_dropdown)
        self.radio_audio.select()
        self.radio_audio.grid(row=1, column=1, padx=10, pady=10, sticky="e")

        self.label_path = tk.Label(self.master, text="Save Location:",font=("Arial",10))
        self.label_path.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        self.var_path = tk.StringVar(value=os.getcwd())
        self.entry_path = tk.Entry(self.master, textvariable=self.var_path, width=40)
        self.entry_path.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        self.button_browse = tk.Button(self.master, text="Browse", command=self.browse_path,font=("Arial",10))
        self.button_browse.grid(row=2, column=2, padx=10, pady=10)

        self.label_resolution = tk.Label(self.master, text="Select Resolution:",font=("Arial",10))
        self.label_resolution.grid(row=3, column=0, padx=10, pady=10, sticky="w")
        
        self.var_resolution = tk.StringVar()
        self.resolution_dropdown = ttk.Combobox(self.master, textvariable=self.var_resolution, state="disabled")
        self.resolution_dropdown.grid(row=3, column=1, padx=10, pady=10, sticky="w")

        self.button_download = tk.Button(self.master, text="Download",bg="#3697f5",fg="#fff",cursor="hand2",command=self.before_download,font=("Arial",10))
        self.button_download.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        # self.progress_bar = ttk.Progressbar(self.master, orient="horizontal", length=300, mode="indeterminate")
        # self.progress_bar.grid(row=5, columnspan=2, padx=10, pady=10)

        self.Message_label = tk.Label(self.master, text="")
        self.Message_label.grid(row=6, columnspan=2, padx=10, pady=10)

    def toggle_resolution_dropdown(self):
        if self.var_type.get() == "video":
            self.resolution_dropdown.config(state="enabled")
            self.populate_resolution_options()
        else:
            self.resolution_dropdown.config(state="disabled")

    def populate_resolution_options(self):
        self.var_resolution.set("")  # Clear previous selection
        self.resolution_dropdown["values"] = ["1080p", "720p", "480p", "360p", "240p", "144p"]

    def browse_path(self):
        path = filedialog.askdirectory()
        if path:
            self.var_path.set(path)

    def before_download(self):
        url = self.entry_url.get()
        if not url:
            self.show_message("Please enter a valid YouTube URL.")
            self.button_download.config(state="normal")
            return
        else:    
            self.button_download.config(state="disabled")
            self.Message_label.config(text="Downloading starts...")
            self.master.update()
            self.download()

    def download(self):
        url = self.entry_url.get()
        download_type = self.var_type.get()
        save_path = self.var_path.get()
        loc_resolution = self.var_resolution.get()

        try:
            yt = YouTube(url)

            if download_type == "video":
                stream = yt.streams.filter(progressive=True)
                l_res = [s.resolution for s in stream]
                # print(l_res)
                if loc_resolution in l_res:
                    stream = yt.streams.filter(progressive=True, file_extension="mp4", resolution=loc_resolution).first()
                    # file_size = stream.filesize
                else:
                    stream = yt.streams.filter(progressive=True, file_extension="mp4").first()
                    # file_size = stream.filesize
            else:
                stream = yt.streams.filter(only_audio=True).first()
                # file_size = stream.filesize

            stream.download(output_path=save_path)

            self.Message_label.config(text="Downloading finishes...")
            self.master.update()
            self.button_download.config(state="normal")

        except Exception as e:
            self.Message_label.config(text="")
            self.master.update()
            self.show_message("Please enter a valid YouTube URL.")

    def show_message(self, message):
        popup = tk.Toplevel()
        popup.title("Message")
        popup.geometry("250x100")
        label = tk.Label(popup, text=message)
        label.pack(padx=20, pady=20)
        button = tk.Button(popup, text="OK", command=popup.destroy)
        button.pack(pady=10)

def main():
    root = tk.Tk()
    app = YouTubeDownloaderApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()