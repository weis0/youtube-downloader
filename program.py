import youtube_dl, os
import tkinter as tk
from tkinter import ttk, filedialog
from tkinter.scrolledtext import ScrolledText


class YTLogger(object):
    def debug(self, msg):
        AddLog(msg + "\n")
    def warning(self, msg):
        AddLog(msg + "\n")
    def error(self, msg):
        AddLog(msg + "\n")

class Public(): pass

class Log():
    def error(msg):
        tk.messagebox.showerror("Error:", msg)
    def my_hook(d):
        if d["status"] == "finished":
            AddLog("Download finished - now converting\n")

def AddLog(text):
    Public.logger.config(state="normal")
    Public.logger.insert("end", text)
    Public.logger.config(state="disabled")

class App():
    def __init__(self, master):
        super().__init__()
        self.CreateUI(master)

    def CreateUI(self, master):
        self.logo = ttk.Label(master, text="BΣЯƬӨ YӨЦƬЦBΣ DӨЩПLӨΛDΣЯ", font=("Helvetica", 16))
        self.logo.pack(side="top", padx=5)
 

        #______________________________________________________________________#
        """ Build url and desired file format getter """
        getUrlInf = ttk.Frame(master)
        getUrlLs = ttk.Frame(getUrlInf)
        self.urlL = ttk.Label(getUrlLs, text="Youtube Url", font=("Helvetica", 12))
        self.urlL.pack(anchor="w")
        self.getUrlE = ttk.Entry(getUrlLs, width=50)
        self.getUrlE.pack(side="left", fill="x", expand=1, padx=2)
        getUrlLs.pack(side="left")

        getForm = ttk.Frame(getUrlInf)
        self.formL = ttk.Label(getForm, text="Video Format", font=("Helvetica", 12))
        self.formL.pack(anchor="e")
        self.format = tk.StringVar()
        self.formats = ["video", "audio"]
        self.format.set(self.formats[0])
        self.getFormat = ttk.Combobox(getForm, textvariable=self.format, values=self.formats, width=13)
        self.getFormat.current(0)
        self.getFormat.config(state="readonly")
        self.getFormat.pack(side="left", padx=2)
        getForm.pack(side="right")
        getUrlInf.pack()

        self.location = os.getcwd()

        ttk.Label(text="Download location", font=("Helvetica",12)).pack(side="top", anchor="w")
        getLocF = ttk.Frame(master)
        self.getLocE = ttk.Entry(getLocF, width=60)
        self.getLocE.pack(side="left", fill="x", expand=1, padx=2)
        self.getLocB = ttk.Button(getLocF, text="...", command=self.GetSaveDir)
        self.getLocB.config(width=4)
        self.getLocB.pack(side="right", padx=2)
        getLocF.pack()

        #______________________________________________________________________#
        """ Build Logger, Progress bar and download button """

        Public.logger = ScrolledText(master, relief="flat", width=40)
        Public.logger.config(height=6, state="disabled")
        Public.logger.pack(padx=5, pady=5, fill="x")#, expand=1)
        AddLog("-"*48 + "\nYoutube Download Log\n" + "-"*48 + "\n\n")

        self.bar = ttk.Progressbar(master, orient="horizontal", length=400, mode="determinate")
        self.bar.pack(pady=5)
        #self.bar.config(mode="indeterminate")
        #self.bar.start(30)

        self.downloadB = ttk.Button(master, text="░D░o░w░n░l░o░a░d░", command=lambda: self.Download(master))
        self.downloadB.config(width=20)
        self.downloadB.pack(pady=2)

    def GetSaveDir(self):
        self.location = filedialog.askdirectory()
        self.getLocE.delete(0, "end")
        self.getLocE.insert(0, self.location)

    def Download(self, master):
        urlYT = self.getUrlE.get()
        if urlYT == "":
            Log.error("Please enter a url")
            return
        formatYT = self.getFormat.get()
        if formatYT == None:
            formatYT = "video"
        if not self.location:
            self.loaction = os.getcwd()

        self.downloadB.config(state="disabled")
        if formatYT == "audio":
            ydl_opts = {"format": "bestaudio/best",
                        "postprocessors": [{
                            "key": "FFmpegExtractAudio",
                            "preferredcodec": "mp3",
                            "preferredquality": "192"}],
                        "logger": YTLogger(),
                        "outtmpl": str(self.location) + "\\%(title)s.%(ext)s",
                        "progress_hooks": [Log.my_hook]}
        else:# formatYT == "video"
            ydl_opts = {"logger": YTLogger(),
                        "outtmpl": self.location + "\\%(title)s.%(ext)s",
                        "progress_hooks": [Log.my_hook]}

        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([urlYT])
        except Exception as err:
            AddLog(err)
            Log.error("Exception, please refer to log")

        self.downloadB.config(state="normal")

def Start():
    root = tk.Tk()
    root.title("Berto's python Downloader")
    root.resizable(0,0)
    root.configure(background='#590000')
    App(root)
    root.mainloop()

if __name__ == "__main__":
    Start()
