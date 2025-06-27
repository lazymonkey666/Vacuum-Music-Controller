import os
import tkinter.filedialog
import tkinter.messagebox
import pygame
import time
import keyboard
import sys
import tkinter
import threading
import winreg
from tkinter import ttk
ccc=0
def get_theme_color_via_registry():
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\DWM")
        value, _ = winreg.QueryValueEx(key, "ColorizationColor")
        winreg.CloseKey(key)
        return value
    except FileNotFoundError:
        return None
def is_darkmode():
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize")
        d, regtype = winreg.QueryValueEx(key, "AppsUseLightTheme")
        winreg.CloseKey(key)
        return d # 如果值为 0，表示系统处于深色模式
    except FileNotFoundError:
        return False
print(is_darkmode())
if is_darkmode()==1 or is_darkmode()==False:
    bgcolor="white"
    fgcolor="black"
if is_darkmode()==0:
    bgcolor="black"
    fgcolor="white"
color_value = get_theme_color_via_registry()
if color_value:
    color="#"+hex(color_value)[4:]
r = int(color[1:3], 16)
g = int(color[3:5], 16)
b = int(color[5:7], 16)
luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
if luminance > 0.5:
    text_color="#000000"  # 黑色
else:
    text_color='#FFFFFF'  # 白色

quit_flag = 0
show = 0

window = tkinter.Tk()
window.overrideredirect(1)
window.attributes("-topmost", 1)
window.geometry("500x230")
window.configure(bg=bgcolor)
window.withdraw()

path___ = sys.argv
path__ = path___[0].split("\\")
path__.pop()
path = '\\\\'.join(path__)
print(path)

# New code:
if not os.path.exists("config.ini"):
    music_path=tkinter.filedialog.askdirectory(title="请选择音乐文件夹")
    with open('config.ini', 'x') as file:
        file.write(music_path)


with open('config.ini', 'r') as f:
    playpath = f.read()
playlist = []
try:
    for name in os.listdir(playpath):
        a = name.split(".")
        if "." in name:
            if a[-1] == "mp3":
                playlist.append(name)
except FileNotFoundError:
    tkinter.messagebox.showwarning("警告","路径不存在")
    music_path=tkinter.filedialog.askdirectory(title="请选择音乐文件夹")
    with open('config.ini', 'w') as file:
        file.write(music_path)
    pathfile=music_path
    for name in os.listdir(playpath):
        a = name.split(".")
        if "." in name:
            if a[-1] == "mp3" or "wav":
                playlist.append(name)

file_mod_times = {f: os.path.getmtime(os.path.join(playpath, f)) for f in playlist}
__final_playlist = sorted(file_mod_times.items(), key=lambda item: item[1], reverse=True)
final_playlist = []
for x, y in __final_playlist:
    final_playlist.append(x)
def listbox_refresh():
    listbox.delete(0,tkinter.END)
    for song_id in range(len(final_playlist)):
        if len(str(final_playlist[(song_id+current_index)% len(final_playlist)])) > 60:
            listbox.insert(tkinter.END, final_playlist[(song_id+current_index)% len(final_playlist)][0:60] + "...")
        else:
            listbox.insert(tkinter.END, final_playlist[(song_id+current_index)% len(final_playlist)])
    listbox.itemconfig(0,bg=color,fg=text_color)
    music_long=int(pygame.mixer.Sound(os.path.join(playpath, final_playlist[current_index])).get_length() * 1000)
    minutes = str(music_long // 60000)
    if len(minutes)==1:
        minutes="0"+minutes
    seconds = str((music_long % 60000) // 1000)
    if len(seconds)==1:
        seconds="0"+seconds
    total_time_label["text"]=str(minutes)+":"+str(seconds)
   
    play_music(current_index)
def check_selected():
    global current_index
    selection = listbox.curselection()
    if selection:

        print(f"Selected item index: {selection[0]}")
        print(f"Selected item: {listbox.get(selection[0])}")
        current_index = (current_index + selection[0]) % len(final_playlist)
        listbox_refresh()
        
    else:
        print("No item selected.")

listbox = tkinter.Listbox(window, width=70,height=9)
listbox.pack(fill="x")
listbox.configure(background=bgcolor,fg=fgcolor)
button=tkinter.Button(window,text="Play",bg=bgcolor,fg=fgcolor,command=check_selected)
button.pack(fill="x")
style = ttk.Style()
# 设置进度条的颜色（这里设置为蓝色，你可以使用颜色名称或十六进制颜色代码）
style.theme_use('default')  # 确保使用默认主题，以便自定义样式生效
style.configure("Custom.Horizontal.TProgressbar", troughcolor=bgcolor,
                bordercolor='gray', background=color)
# 创建进度条
progress = ttk.Progressbar(window, style="Custom.Horizontal.TProgressbar",
                            orient='horizontal', length=200, mode='determinate')
progress.pack(fill="both")
progress["value"]=50
now_time_label=tkinter.Label(window,text="00:00",bg=bgcolor,fg=fgcolor)
now_time_label.pack(side="left")
total_time_label=tkinter.Label(window,text="01:00",bg=bgcolor,fg=fgcolor)
total_time_label.pack(side="right")
def progress_click(event):
    global ccc
    pos_percent=event.x/500
    pygame.mixer.music.set_pos(pos_percent*music_long/1000)
    ccc=(pos_percent*music_long)-pygame.mixer.music.get_pos()
progress.bind("<Button - 1>",progress_click)

lock = threading.Lock()
timer=0

def play_music(index):
    pygame.mixer.init()
    pygame.mixer.music.load(os.path.join(playpath, final_playlist[index]))
    pygame.mixer.music.play()


def control_music():
    global show,current_index,music_long,ccc
    current_index = 0
    playing = True
    play_music(current_index)
    music_long=int(int(pygame.mixer.Sound(os.path.join(playpath, final_playlist[current_index])).get_length() * 1000))
    minutes = str(music_long // 60000)
    if len(minutes)==1:
        minutes="0"+minutes
    seconds = str((music_long % 60000) // 1000)
    if len(seconds)==1:
        seconds="0"+seconds
    total_time_label["text"]=str(minutes)+":"+str(seconds)

    while True:
        if not pygame.mixer.music.get_busy():
            if playing:
                ccc=0
                current_index = (current_index + 1) % len(final_playlist)
                print(f"自动播放: {final_playlist[current_index]}")
                listbox_refresh()
                

        # 检测按键
        if keyboard.is_pressed('ctrl+alt+>'):
            ccc=0
            with lock:
                current_index = (current_index + 1) % len(final_playlist)
                pygame.mixer.music.stop()
                print(f"跳到下一曲: {final_playlist[current_index]}")
                listbox_refresh()
            time.sleep(0.5)

        elif keyboard.is_pressed('ctrl+alt+<'):
            ccc=0
            with lock:
                current_index = (current_index - 1) % len(final_playlist)
                pygame.mixer.music.stop()
                print(f"跳到上一曲: {final_playlist[current_index]}")
                listbox_refresh()
            time.sleep(0.5)

        elif keyboard.is_pressed('ctrl+alt+/'):
            with lock:
                if playing:
                    pygame.mixer.music.pause()
                    playing = False
                    print("音乐已暂停")
                else:
                    pygame.mixer.music.unpause()
                    playing = True
                    print("音乐已恢复")
            time.sleep(0.5)

        elif keyboard.is_pressed('ctrl+alt+x') or quit_flag == 1:
            pygame.mixer.music.stop()
            print("退出音乐播放器")
            window.quit()
            break
        elif keyboard.is_pressed('ctrl+alt+l'):
            with lock:
                if show == 0:
                    window.deiconify()
                    show = 1
                else:
                    window.withdraw()
                    show = 0
            time.sleep(0.5)
        
        time.sleep(0.1)
        
        #更新进度条
        current_pos=pygame.mixer.music.get_pos()+int(ccc)
        progress["value"]=current_pos/music_long*100
        minutes = str(current_pos // 60000)
        if len(minutes)==1:
            minutes="0"+minutes
       
        seconds = str((current_pos % 60000) // 1000)
        if len(seconds)==1:
            seconds="0"+seconds
        now_time_label["text"]=str(minutes)+":"+str(seconds)


def music_player():
    try:
        control_music()
    finally:
        pygame.mixer.quit()


def on_closing():
    global quit_flag
    quit_flag = 1
    window.destroy()

thread1 = threading.Thread(target=music_player)
thread1.start()
# 在初始化时，将所有音乐插入列表框
for song in final_playlist:
    if len(song) > 60:
        listbox.insert(tkinter.END, song[0:60] + "...")
    else:
        listbox.insert(tkinter.END, song)
listbox.itemconfig(0,bg=color,fg=text_color)

window.withdraw()
window.protocol("WM_DELETE_WINDOW", on_closing)
window.mainloop()