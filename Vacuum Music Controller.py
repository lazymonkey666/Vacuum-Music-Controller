import os
import pygame
import time
import keyboard
import sys
path___=sys.argv
path__=path___[0].split("\\")
path__.pop()
path='\\\\'.join(path__)
print(path)
#New code:
if not os.path.exists("config.ini"):
    with open('config.ini', 'x') as file:
        file.write("e:\\1 音乐\\")
        
    os.system("notepad "+path+"\\config.ini")
#Old code:
"""try:
    os.path.exists("e:\\1 音乐\\")
    drive="e"
except:
    try:
        os.path.exists("f:\\1 音乐\\")
        drive="f"
    except:
        os.path.exists("g:\\1 音乐\\")
        drive="g"
"""

with open('config.ini', 'r') as f:
    playpath = f.read()
playlist=[]
for name in os.listdir(playpath):
    a=name.split(".")
    if "." in name:
        if a[-1]=="mp3" :
            playlist.append(name)

file_mod_times = {f: os.path.getmtime(os.path.join(playpath, f)) for f in playlist}
__final_playlist = sorted(file_mod_times.items(), key=lambda item: item[1],reverse=True)
final_playlist=[]
for x,y in __final_playlist:
    final_playlist.append(x)

def play_music(index):
    pygame.mixer.init()
    pygame.mixer.music.load(os.path.join(playpath, final_playlist[index]))
    pygame.mixer.music.play()

def control_music():
    current_index = 0
    playing = True 
    play_music(current_index) 

    while True:
        if not pygame.mixer.music.get_busy():  
            if playing: 
                current_index = (current_index + 1) % len(final_playlist)  
                play_music(current_index)
                print(f"自动播放: {final_playlist[current_index]}")

        # 检测按键
        if keyboard.is_pressed('ctrl+alt+>'):
            current_index = (current_index + 1) % len(final_playlist)  
            pygame.mixer.music.stop()  
            play_music(current_index)  
            print(f"跳到下一曲: {final_playlist[current_index]}")
            time.sleep(0.5)

        elif keyboard.is_pressed('ctrl+alt+<'):
            current_index = (current_index - 1) % len(final_playlist)  
            pygame.mixer.music.stop()  
            play_music(current_index)  
            print(f"跳到上一曲: {final_playlist[current_index]}")
            time.sleep(0.5)

        elif keyboard.is_pressed('ctrl+alt+/'):
            if playing:
                pygame.mixer.music.pause()  
                playing = False
                print("音乐已暂停")
                time.sleep(0.5)
            else:
                pygame.mixer.music.unpause()  
                playing = True
                print("音乐已恢复")
                time.sleep(0.5)

        elif keyboard.is_pressed('ctrl+alt+x'):  
            pygame.mixer.music.stop()
            print("退出音乐播放器")
            break

        time.sleep(0.1) 


control_music()