# Python Music Player is an Application written in Python Programming Language

# importing modules
# Note: We have to explicitly import 'messagebox' and 'filedialog' from 'tkinter' though we imported everything from tkinter 
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

# the below line hides the 'pygame' module description in the console (this should be done before importing pygame module)
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from pygame import mixer

# creating a GUI window
window = th.ThemedTk()

# using themes from 'ttkthemes'
window.get_themes()
window.set_theme("arc")

# setting the title and icon for the GUI window
window.title("Python Music Player")
window.iconbitmap("Icon.ico")

# to pop up the GUI window at the center of the screen
gui_width = 625
gui_height = 350

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x_coordinate = (screen_width/2) - (gui_width/2)
y_coordinate = (screen_height/2) - (gui_height/2)

window.geometry(f'{gui_width}x{gui_height}+{int(x_coordinate)}+{int(y_coordinate)}')


# this line restricts the user to resize the window ( the two parameters 'width' and 'height' are given false for resizing)
window.resizable(FALSE,FALSE)

# initializing the 'mixer'
mixer.init()

# function to close the GUI window
def close():
	stop_music()
	window.destroy()

# fuction to display the currently playing song
def show_playing_song():
	try:
		statusbar['text'] = "Playing Music - " + os.path.basename(currently_selected_song)
	except:
		pass
# 'os.path.basename(file_name)' returns the file name neglecting the directory path  
# for example os.path.basename('/home/User/Desktop/file.txt') returns 'file.txt'

# function to display the 'total duration of the music' and to start a thread for implementing 'remaining time'
def music_details(selected_song):

	# 'os.path.splittext(file_name)' return a list of two elements (i.e) the extension of the file and the rest other than extension
	# for example os.path.splitext('/home/User/Desktop/file.txt') returns ['/home/User/Desktop/file' , '.txt ']
	extension = os.path.splitext(selected_song)

	# if the music file is .mp3, total duration of music can be found using 'MP3' from 'mutagen.mp3' 
	if extension[-1] == ".mp3":
		mp3_audio = MP3(selected_song)
		duration_of_music = mp3_audio.info.length

	# else for other music files, total duration of music can be found using 'mixer' from 'pygame'
	else:
		length = mixer.Sound(selected_song)
		duration_of_music = length.get_length()

	# 'divmod' returns 'Quotient' and 'Remainder' when the first parameter is divided by the second
	minutes,seconds = divmod(duration_of_music,60)

	minutes,seconds = round(minutes),round(seconds)
	minutes = str(minutes).zfill(2)
	seconds = str(seconds).zfill(2)

	music_duration_label['text'] = "Total Duration - %s:%s"%(minutes,seconds)

	# starting a thread for displaying the remaining duration of music
	thread_var = Thread(target=show_remaining_time,args=(duration_of_music,))
	thread_var.start()

# function for showing the remaining duration of music 
def show_remaining_time(val):
	global paused 

	# if val != 0 (i.e) the music is playing and 'get_busy()' return True if the pygame.mixer is playing some music
	while val and mixer.music.get_busy():
		
		if paused:
			continue
		else:

			# 'divmod' returns 'Quotient' and 'Remainder' when the first parameter is divided by the second
			minutes,seconds = divmod(val,60)

			minutes,seconds = round(minutes),round(seconds)
			minutes = str(minutes).zfill(2)
			seconds = str(seconds).zfill(2)
			remaining_time['text'] = "Remaining Time - %s:%s"%(minutes,seconds)	
			time.sleep(1)
			val -= 1	

# function to play the music
def play_music():
	global paused, currently_selected_song
	
	# if the music is paused, the music will resume instead of playing from beginning
	# 'mixer.music.unpause()' unpauses a paused music 
	if paused:
		mixer.music.unpause()
		statusbar['text'] = "Music has been Resumed"
		paused = False
		statusbar.after(3000,show_playing_song)
		# after() method accepts two parameters, 1.time in milliseconds and 2.function to be executed after the given time

	else:
		
		try:

			# the currently playing music has to be stopped before playing the new music if the user doesn't stopped it manually
			# mixer.music.get_busy() returns true if the mixer.music is busy that is some music is playing
			if mixer.music.get_busy():
				stop_music()
				time.sleep(1)

			# curselection() method returns a tuple containing the line numbers of the selected element or elements, counting from 0.
			# If nothing is selected, returns an empty tuple.
			# Here it is used to play the selected song from the playlist
			currently_selected = playlist_box.curselection()
			currently_selected_song_index = currently_selected[0]
			currently_selected_song = playlist[int(currently_selected_song_index)]

			# loading and start playing the song using 'load' and 'play' methods
			mixer.music.load(currently_selected_song)
			mixer.music.play()

			statusbar['text'] = "Playing Music - " + os.path.basename(currently_selected_song)

			# calling 'music_details()' function to display the duration of music and remaining duration of music
			music_details(currently_selected_song)

		# if no song is selected or added, a messagebox is displayed with a message
		except:
			messagebox.showerror("Error", "Please choose a music file to play") 

# function to stop the music
# 'mixer.music.stop()' is used to stop the music
def stop_music():
	if mixer.music.get_busy():
		mixer.music.stop()
		statusbar['text'] = "Music has been Stopped"
		music_duration_label.config(text = "Total Duration : --|--")
		remaining_time.config(text = "Remaining Time : --|--")

# declaring a global variable 'paused' to indicate whether the music is paused or not
paused = False

# function to pause the music
# 'mixer.music.pause()' is used to pause the music
def pause_music():
	global paused
	if mixer.music.get_busy():
		paused = True 
		mixer.music.pause()
		statusbar['text'] = "Music has been Paused"

# function to set the volume of the music
def set_vol(volume):
	mixer.music.set_volume(float(volume)/100)

# function to display the 'About Us' messagebox
def about_us():
	messagebox.showinfo("About Us", " Python Music Player is built with Python's best Library for GUI 'tkinter' with some of the packages like 'pygame' and 'os'")

playlist = []

# function to add music to the playlist
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

# function to delete the music file from the playlist
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

# function to rewind the music
def rewind_music():
	play_music()
	statusbar['text'] = "Music Rewinded"
	statusbar.after(3000,show_playing_song)

# declaring global variable 'mutes' to indicate whether the music is muted or not
muted = False

# function to mute or unmute music
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

# functions executed when cursor hovers over any buttonn
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

# displaying statusbar at the bottom of the window
statusbar = Label(window, text = "Welcome to Python Music Player", relief = RIDGE, anchor = W)
statusbar.pack(side = BOTTOM, fill= X)

right_label_status_bar = Label(statusbar, text="")
right_label_status_bar.pack(anchor=E)

# displaying menubar at the top of the window using 'config'
menubar = Menu(window)	
window.config(menu = menubar)

# adding submenu in the menubar
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

# implementing keyboard shortcuts using 'on_press_key' function from 'keyboard' module
on_press_key("a", lambda _ : browse_file())
on_press_key("delete", lambda _ : delete_from_playlist_box())
on_press_key("enter", lambda _ : play_music())
on_press_key("p", lambda _ : pause_music())
on_press_key("s", lambda _ : stop_music())
on_press_key("m", lambda _ : mute_or_unmute_music())
on_press_key("r", lambda _ : rewind_music())
on_press_key("esc", lambda _ : close())

# inserting images for buttons using 'PhotoImage' Widget
play_button_image = PhotoImage(file = "Play.png")
stop_button_image = PhotoImage(file = "Stop.png")
pause_button_image = PhotoImage(file = "Pause.png")
rewind_button_image = PhotoImage(file = "Rewind.png")
mute_button_image = PhotoImage(file = "Mute.png")
unmute_button_image = PhotoImage(file = "Unmute.png")

# creating and displaying various widgets
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

# creating and displaying a 'Listbox' widget for Playlist
playlist_box = Listbox(left_frame)
playlist_box.pack()

# creating and displaying a 'Add' button to add music files to the playlist
add_button = ttk.Button(left_frame, text = " Add + ", command = browse_file, cursor = "hand2")
add_button.pack(side = LEFT)

# creating and displaying a 'Delete' button to delete music files from the playlist
del_button = ttk.Button(left_frame, text = " - Delete", command = delete_from_playlist_box, cursor = "hand2")
del_button.pack(side = LEFT)

# Label widgets for 'Total Duration' and 'Remaining Time'
music_duration_label = ttk.Label(right_frame_top , text = "Total Duration : --|--")
remaining_time = ttk.Label(right_frame_top , text = "Remaining Time : --|--")
music_duration_label.pack()
remaining_time.pack(pady=10)

# creating buttons for the Player Functionalities
play_button = ttk.Button(right_frame_middle, image = play_button_image, command = play_music, cursor = "hand2")
stop_button = ttk.Button(right_frame_middle, image = stop_button_image, command = stop_music, cursor = "hand2")
pause_button = ttk.Button(right_frame_middle, image = pause_button_image, command = pause_music, cursor = "hand2")
rewind_button = ttk.Button(right_frame_bottom, image = rewind_button_image, command = rewind_music, cursor = "hand2")
mute_or_unmute_button = ttk.Button(right_frame_bottom, image = unmute_button_image, command = mute_or_unmute_music, cursor = "hand2")

# creating a Volume Slider
volume_scale = ttk.Scale(right_frame_bottom, from_ = 0, to = 100, orient = HORIZONTAL, command = set_vol, cursor = "hand2")
volume_scale.set(50)
mixer.music.set_volume(.5)

# displaying the buttons on to the windows
play_button.grid(row = 0, column = 0, padx = 5)
stop_button.grid(row = 0, column = 1, padx = 5)
pause_button.grid(row = 0, column = 2, padx = 5)
rewind_button.grid(row = 0, column = 0)
mute_or_unmute_button.grid(row = 0, column = 1)

# displaying the Volume Slider on to the screen
volume_scale.grid(row = 0, column = 2, pady = 15, padx = 30)

# binding the buttons with the functions to display what the button is when cursor hovers over them 
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


# overriding the close(X) button of the window
window.protocol("WM_DELETE_WINDOW", close)

# to start the GUI window, 'mainloop' method is used
window.mainloop()
