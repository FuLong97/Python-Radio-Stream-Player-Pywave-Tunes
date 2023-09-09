from tkinter import *
from ttkbootstrap import *
from ttkbootstrap.style import Style
import ttkbootstrap as ttk
import vlc
from ttkbootstrap.constants import *
from ttkbootstrap.toast import ToastNotification
import requests
import threading

player = None

def play_radio():
    global player
    stream = selected_stream.get()
    player = vlc.MediaPlayer(stream)
    player.play()

def pause_radio():
    global player
    player.stop()

def change_volume(event):
    global player
    volume = int(volume_slider.get())
    if player:
        player.audio_set_volume(volume)
    volume_percentage = volume / 100  # Calculate volume percentage
    volume_label.configure(text="Volume: {:.0%}".format(volume_percentage))

def load_m3u_playlist(file_path):
    with open(file_path, 'r') as m3u_file:
        lines = m3u_file.readlines()

    # Filtere die Zeilen, die tatsächliche Stream-URLs enthalten (ignoriere Kommentare und Zeilenumbrücke)
    stream_urls = [line.strip() for line in lines if not line.startswith('#') and line.strip()]

    return stream_urls

# Beispiel: M3U-Datei "radio_streams.m3u"
m3u_file_path = 'radio_streams.m3u'
streams = load_m3u_playlist(m3u_file_path)

root = ttk.Window(themename="darkly")
root.geometry("800x600")
root.title("Radio")

volume_slider = ttk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, length=400)
volume_slider.set(100)
volume_slider.pack(side=tk.TOP, padx=5, pady=5)

pause_button = ttk.Button(root, text='Pause', bootstyle=DARK, command=pause_radio)
pause_button.pack(side=BOTTOM, padx=10, pady="10")

play_button = ttk.Button(root, text='Play', bootstyle=DARK, command=play_radio)
play_button.pack(side=BOTTOM, padx=5, pady=10)

label = ttk.Label(root, text="PyWaveTunes", font=("Arial", 30))
label.pack(side=TOP, padx=5, pady=5)

selected_stream = StringVar()
stream_cb = ttk.Combobox(root, values=streams, textvariable=selected_stream, font=("Arial", 15), width=50, state="readonly")
stream_cb.pack(side=TOP, padx=5, pady=50)

volume_label = ttk.Label(root, text="Volume:", font=("Arial", 15))
volume_label.pack(side=TOP, padx=5, pady=5)

volume_slider.bind("<ButtonRelease-1>", change_volume)
volume_slider.bind("<B1-Motion>", change_volume)
stream_cb.bind("<<ComboboxSelected>>", change_volume)
play_button.bind("<ButtonRelease-1>", change_volume)

tabControl = ttk.Notebook(root)
tab1 = ttk.Frame(tabControl)
tabControl.add(tab1, text="Streams")
tabControl.pack(side="top", expand=1, fill="both")

tab2 = ttk.Frame(tabControl)
tabControl.add(tab2, text="Settings")
tabControl.pack(side="top", expand=1, fill="both")

root.mainloop()
