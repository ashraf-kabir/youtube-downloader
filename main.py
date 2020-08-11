from pytube import *
from tkinter import *
from tkinter.filedialog import *
from tkinter.messagebox import *
from threading import *

file_size = 0


# this func gets called for updating download progress
def progress(stream, chunk, file_handle, remaining=None):
    # get the percentage of the file which is downloading
    file_downloaded = (file_size - file_handle)
    per = ((file_downloaded / file_size) * 100)
    dBtn.config(text="{:00.0f}% Downloaded".format(per))


def startDownload():
    global file_size
    try:
        url = urlField.get()
        print(url)
        # changing btn text
        dBtn.config(text='Please wait...')
        dBtn.config(state=DISABLED)
        path_to_save_video = askdirectory()
        print(path_to_save_video)
        if path_to_save_video is None:
            return
        # creating youtube object with URL
        ob = YouTube(url, on_progress_callback=progress)
        strm = ob.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        file_size = strm.filesize
        # print(strm.title)
        vTitle.config(text=strm.title)
        vTitle.pack(side=TOP)
        print(file_size)
        strm.download(path_to_save_video)
        # print("Download completed...")
        dBtn.config(text='Start Download')
        dBtn.config(state=NORMAL)
        showinfo("Download Completed", "Downloaded successfully")
        urlField.delete(0, END)
        vTitle.pack_forget()

    except Exception as e:
        print(e)
        print("Error")


def startDownloadThread():
    # create thread
    thread = Thread(target=startDownload)
    thread.start()


# starting GUI building
main = Tk()

# title
main.title("My Youtube Downloader")

# set icon
# main.iconbitmap('@icon.ico')

# heading icon
file = PhotoImage(file='youtube-downloader.png')
headingIcon = Label(main, image=file)
headingIcon.pack(side=TOP)

# url textfield
urlField = Entry(main, font=("verdana", 14), justify=CENTER)
urlField.pack(side=TOP, fill=X, padx=10)

# download button
dBtn = Button(main, text="Start Download", font=("verdana", 18), command=startDownloadThread)
dBtn.pack(side=TOP, pady=10)

# video title
vTitle = Label(main, text="Video title")

main.geometry("500x600")
main.mainloop()
