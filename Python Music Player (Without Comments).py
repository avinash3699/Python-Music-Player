
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from mutagen.mp3 import MP3
from threading import Thread
from tkinter import ttk
from ttkthemes import themed_tk as th 
import os
import time
from keyboard import on_press_key

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from pygame import mixer

window = th.ThemedTk()

window.get_themes()
window.set_theme("arc")

window.title("Python Music Player")
window.iconbitmap("Icon.ico")

gui_width = 625
gui_height = 350

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x_coordinate = (screen_width/2) - (gui_width/2)
y_coordinate = (screen_height/2) - (gui_height/2)

window.geometry(f'{gui_width}x{gui_height}+{int(x_coordinate)}+{int(y_coordinate)}')


window.resizable(FALSE,FALSE)

mixer.init()

def close():
	stop_music()
	window.destroy()

def show_playing_song():
	try:
		statusbar['text'] = "Playing Music - " + os.path.basename(currently_selected_song)
	except:
		pass

def music_details(selected_song):

	extension = os.path.splitext(selected_song)

	if extension[-1] == ".mp3":
		mp3_audio = MP3(selected_song)
		duration_of_music = mp3_audio.info.length

	else:
		length = mixer.Sound(selected_song)
		duration_of_music = length.get_length()

	minutes,seconds = divmod(duration_of_music,60)

	minutes,seconds = round(minutes),round(seconds)
	minutes = str(minutes).zfill(2)
	seconds = str(seconds).zfill(2)

	music_duration_label['text'] = "Total Duration - %s:%s"%(minutes,seconds)

	thread_var = Thread(target=show_remaining_time,args=(duration_of_music,))
	thread_var.start()

def show_remaining_time(val):
	global paused 

	while val and mixer.music.get_busy():
		
		if paused:
			continue
		else:

			minutes,seconds = divmod(val,60)

			minutes,seconds = round(minutes),round(seconds)
			minutes = str(minutes).zfill(2)
			seconds = str(seconds).zfill(2)
			remaining_time['text'] = "Remaining Time - %s:%s"%(minutes,seconds)	
			time.sleep(1)
			val -= 1	

def play_music():
	global paused, currently_selected_song

	if paused:
		mixer.music.unpause()
		statusbar['text'] = "Music has been Resumed"
		paused = False
		statusbar.after(3000,show_playing_song)

	else:
		
		try:

			if mixer.music.get_busy():
				stop_music()
				time.sleep(1)

			currently_selected = playlist_box.curselection()
			currently_selected_song_index = currently_selected[0]
			currently_selected_song = playlist[int(currently_selected_song_index)]

			mixer.music.load(currently_selected_song)
			mixer.music.play()

			statusbar['text'] = "Playing Music - " + os.path.basename(currently_selected_song)

			music_details(currently_selected_song)

		except:
			messagebox.showerror("Error", "Please choose a music file to play") 

def stop_music():
	if mixer.music.get_busy():
		mixer.music.stop()
		statusbar['text'] = "Music has been Stopped"
		music_duration_label.config(text = "Total Duration : --|--")
		remaining_time.config(text = "Remaining Time : --|--")

paused = False

def pause_music():
	global paused
	if mixer.music.get_busy():
		paused = True 
		mixer.music.pause()
		statusbar['text'] = "Music has been Paused"

def set_vol(volume):
	mixer.music.set_volume(float(volume)/100)

def about_us():
	messagebox.showinfo("About Us", " Python Music Player is built with Python's best Library for GUI 'tkinter' with some of the packages like 'pygame' and 'os'")

playlist = []

def browse_file():
	global music_file, index
	music_file = filedialog.askopenfilename()

	filename = os.path.basename(music_file)
	extension = os.path.splitext(music_file)

	if extension[-1] in ['.mp3',".wav",".ogg"]:
		if music_file not in playlist:
			playlist_box.insert(index, filename)
			playlist.insert(index,music_file)

			index += 1

		else:
			messagebox.showinfo("File Already Added","The music file you are trying to add is already in the playlist")


	else:
		messagebox.showinfo("Check extension","Please Add a Valid Music File")

def delete_from_playlist_box():
	global playlist_box, playlist, index
	try:
		if mixer.music.get_busy():
			stop_music()
		cur_selected = int(playlist_box.curselection()[0])
		playlist.pop(cur_selected)
		playlist_box.delete(cur_selected)
	except:
		messagebox.showinfo("Select Music", "Please Select a Song to Delete")

def rewind_music():
	play_music()
	statusbar['text'] = "Music Rewinded"
	statusbar.after(3000,show_playing_song)

muted = False

def mute_or_unmute_music():
	global muted

	if muted:
		volume_scale.set(50)
		mixer.music.set_volume(0.5)
		mute_or_unmute_button['image'] = unmute_button_image
		muted = False
	else:
		volume_scale.set(0)
		mixer.music.set_volume(0)
		mute_or_unmute_button['image'] = mute_button_image
		muted = True

def show_add_file_label(e):
	right_label_status_bar.config(text="Add Files")

def show_del_file_label(e):
	right_label_status_bar.config(text="Delete Files")

def show_play_file_label(e):
	right_label_status_bar.config(text="Play Music")

def show_stop_file_label(e):
	right_label_status_bar.config(text="Stop Music")

def show_pause_file_label(e):
	right_label_status_bar.config(text="Pause Music")

def show_rewind_file_label(e):
	right_label_status_bar.config(text="Rewind Music")

def show_mute_or_unmute_file_label(e):
	right_label_status_bar.config(text="Mute/Unmute Music")

def show_volume_scale_file_label(e):
	right_label_status_bar.config(text="Increase/Decrease Volume")

def hide_right_label_status_bar(e):
	right_label_status_bar.config(text="")


index = 0

statusbar = Label(window, text = "Welcome to Python Music Player", relief = RIDGE, anchor = W)
statusbar.pack(side = BOTTOM, fill= X)

right_label_status_bar = Label(statusbar, text="")
right_label_status_bar.pack(anchor=E)

menubar = Menu(window)	
window.config(menu = menubar)

submenu_file = Menu(menubar, tearoff = 0)
submenu_help = Menu(menubar, tearoff = 0)
submenu_shortcuts = Menu(menubar, tearoff = 0)

menubar.add_cascade(label = "File", menu = submenu_file)
submenu_file.add_command(label = "Open", command = browse_file)
submenu_file.add_command(label = "Exit", command = close)

menubar.add_cascade(label = "Help", menu = submenu_help)
submenu_help.add_command(label = "About Us", command = about_us)

menubar.add_cascade(label = "Shortcut Keys", menu=submenu_shortcuts)
submenu_shortcuts.add_command(label="Add file"+"A".rjust(23),command = browse_file)
submenu_shortcuts.add_command(label="Delete file"+"Del".rjust(18),command = delete_from_playlist_box)
submenu_shortcuts.add_command(label="Play/Resume"+"Enter".rjust(11),command = play_music)
submenu_shortcuts.add_command(label="Stop"+"S".rjust(28),command = stop_music)
submenu_shortcuts.add_command(label="Pause"+"P".rjust(26),command = pause_music)
submenu_shortcuts.add_command(label="Mute/Unmute"+"M".rjust(10),command = mute_or_unmute_music)
submenu_shortcuts.add_command(label="Rewind"+"R".rjust(23),command = rewind_music)
submenu_shortcuts.add_command(label="Close"+"Esc".rjust(26),command = rewind_music)

on_press_key("a", lambda _ : browse_file())
on_press_key("delete", lambda _ : delete_from_playlist_box())
on_press_key("enter", lambda _ : play_music())
on_press_key("p", lambda _ : pause_music())
on_press_key("s", lambda _ : stop_music())
on_press_key("m", lambda _ : mute_or_unmute_music())
on_press_key("r", lambda _ : rewind_music())
on_press_key("esc", lambda _ : close())

play_button_image = PhotoImage(file = "Play.png")
stop_button_image = PhotoImage(file = "Stop.png")
pause_button_image = PhotoImage(file = "Pause.png")
rewind_button_image = PhotoImage(file = "Rewind.png")
mute_button_image = PhotoImage(file = "Mute.png")
unmute_button_image = PhotoImage(file = "Unmute.png")

left_frame = Frame(window)
left_frame.pack(side=LEFT, padx =30, pady = 30)

right_frame = Frame(window)
right_frame.pack(side=RIGHT, pady = 30)

right_frame_top = Frame(right_frame)
right_frame_top.pack()

right_frame_middle = Frame(right_frame)
right_frame_middle.pack(padx = 30, pady = 30)

right_frame_bottom = Frame(right_frame)
right_frame_bottom.pack()

wishlist = ttk.Label(left_frame,text="PlayList")
wishlist.pack()

playlist_box = Listbox(left_frame)
playlist_box.pack()

add_button = ttk.Button(left_frame, text = " Add + ", command = browse_file, cursor = "hand2")
add_button.pack(side = LEFT)

del_button = ttk.Button(left_frame, text = " - Delete", command = delete_from_playlist_box, cursor = "hand2")
del_button.pack(side = LEFT)

music_duration_label = ttk.Label(right_frame_top , text = "Total Duration : --|--")
remaining_time = ttk.Label(right_frame_top , text = "Remaining Time : --|--")
music_duration_label.pack()
remaining_time.pack(pady=10)

play_button = ttk.Button(right_frame_middle, image = play_button_image, command = play_music, cursor = "hand2")
stop_button = ttk.Button(right_frame_middle, image = stop_button_image, command = stop_music, cursor = "hand2")
pause_button = ttk.Button(right_frame_middle, image = pause_button_image, command = pause_music, cursor = "hand2")
rewind_button = ttk.Button(right_frame_bottom, image = rewind_button_image, command = rewind_music, cursor = "hand2")
mute_or_unmute_button = ttk.Button(right_frame_bottom, image = unmute_button_image, command = mute_or_unmute_music, cursor = "hand2")

volume_scale = ttk.Scale(right_frame_bottom, from_ = 0, to = 100, orient = HORIZONTAL, command = set_vol, cursor = "hand2")
volume_scale.set(50)
mixer.music.set_volume(.5)

play_button.grid(row = 0, column = 0, padx = 5)
stop_button.grid(row = 0, column = 1, padx = 5)
pause_button.grid(row = 0, column = 2, padx = 5)
rewind_button.grid(row = 0, column = 0)
mute_or_unmute_button.grid(row = 0, column = 1)

volume_scale.grid(row = 0, column = 2, pady = 15, padx = 30)

add_button.bind("<Enter>",show_add_file_label)
add_button.bind("<Leave>",hide_right_label_status_bar)

del_button.bind("<Enter>",show_del_file_label)
del_button.bind("<Leave>",hide_right_label_status_bar)

play_button.bind("<Enter>",show_play_file_label)
play_button.bind("<Leave>",hide_right_label_status_bar)

stop_button.bind("<Enter>",show_stop_file_label)
stop_button.bind("<Leave>",hide_right_label_status_bar)

pause_button.bind("<Enter>",show_pause_file_label)
pause_button.bind("<Leave>",hide_right_label_status_bar)

rewind_button.bind("<Enter>",show_rewind_file_label)
rewind_button.bind("<Leave>",hide_right_label_status_bar)

mute_or_unmute_button.bind("<Enter>",show_mute_or_unmute_file_label)
mute_or_unmute_button.bind("<Leave>",hide_right_label_status_bar)

volume_scale.bind("<Enter>",show_volume_scale_file_label)
volume_scale.bind("<Leave>",hide_right_label_status_bar)


window.protocol("WM_DELETE_WINDOW", close)

window.mainloop()
