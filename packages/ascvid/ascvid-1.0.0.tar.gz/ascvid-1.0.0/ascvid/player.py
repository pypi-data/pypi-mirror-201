from PIL import Image
from math import sqrt
import moviepy.editor as mp
import sys
import os
import time
import cursor
import threading
from .getcol import closest_color
from .logger import print_error,print_warning
CHARS = ' .\'`^",:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$'
CLOSEST_CACHE = {}
CHAR_CACHE = {}
def closest(col):
    global CLOSEST_CACHE
    if col in CLOSEST_CACHE:
        return CLOSEST_CACHE[col]
    cl=closest_color(col)
    CLOSEST_CACHE[col]=cl
    return cl
    
def get_brightness(col):
    R,G,B=col
    return sqrt(0.299 * R**2 + 0.587 * G**2 + 0.114 * B**2)
def _getchar(color):
    if color in CHAR_CACHE:
        return CHAR_CACHE[color]
    brightness=round(get_brightness(color))
    charindex=int((brightness/255)*(len(CHARS)-1))
    char=CHARS[charindex]
    CHAR_CACHE[color]=char
    return char

def get_character(color,colored,truecolor):
    r,g,b=color
    brightness=round(get_brightness(color))
    charindex=int((brightness/255)*(len(CHARS)-1))
    character=CHARS[charindex]
    if colored:
        if truecolor:
            return f"\x1b[38;2;{r};{g};{b}m{character}"
        return f"{closest(color)}{character}"
    return character
def get_pixel(color,colored,truecolor,use_ascii,char):
    if use_ascii:
        return get_character(color,colored,truecolor)
    if truecolor:
        r,g,b=color
        return f"\x1b[38;2;{r};{g};{b}m{char}"
    return f"{closest(color)}{char}"

def show_frame(fr,char,colored,truecolor,use_ascii,resize):
    ts=os.get_terminal_size()
    tw=ts.columns
    th=ts.lines

    sys.stdout.write('\033[H')
    sys.stdout.flush()
    d=Image.fromarray(fr)
    if resize:
        dh=d.height//2
        wd=d.width/tw
        hd=dh/th
        scale=1
        if wd>1 and hd>1 and wd>=hd:
            scale=tw/d.width
        elif wd>1 and hd>1:
            scale=th/dh
        elif wd>1:
            scale=tw/d.width
        elif hd>1:
            scale=th/dh

        d=d.resize((int(d.width*scale),int(dh*scale)))
    pix=d.load()
    lines=[]

    for y in range(d.height):
        line=''
        for x in range(d.width):
            r,g,b,*foo=pix[x,y]
            line+=get_pixel((r,g,b),colored,truecolor,use_ascii,char)
        lines.append(line+'\x1b[0m')
    os.system("clear")
    print('\n'.join(lines),end="")
def mkpos(a):
    if a<0:
        return 0
    return a
def play_vid(file,hide_cursor=True,play_audio=True,fps=None,char="\u2588",colored=True,truecolor=True,use_ascii=False,fast=False):
    vid=mp.VideoFileClip(file)
    if fast:
        frame_count=int(vid.fps*vid.duration)
        if frame_count>=10000:
            response=print_warning(f"{file!r} has {frame_count} frames.",ask="Are you sure you want to resize them all at once [y*]")
            if response!="y":
                sys.exit(1)
        tw=os.get_terminal_size().columns
        th=os.get_terminal_size().lines

        vh=vid.h
        vw=vid.w
        dh=vh//2
        wd=vw-tw
        hd=dh-th
        scale=1
        if wd>0 and hd>0 and wd>=hd:
            scale=tw/vw
        elif wd>0 and hd>0:
            scale=th/dh
        elif wd>0:
            scale=tw/vw
        elif hd>0:
            scale=th/dh

        vid=vid.resize((int(vw*scale),int(dh*scale)))

    fps = fps or vid.fps
    if fps!=vid.fps and fps!="max":
        vid=vid.set_fps(fps)
    process=None
    if hide_cursor:
        cursor.hide()
    if play_audio and vid.audio is not None:
        thread=threading.Thread(target=vid.audio.preview,daemon=True)
        thread.start()
    os.system("clear")
    try:
        for frame in vid.iter_frames():
            t=time.time()
            show_frame(frame,char,colored,truecolor,use_ascii,not fast)
            if fps!="max":
                time.sleep(mkpos(1/fps-(time.time()-t)))
    finally:
        cursor.show()
        sys.stdout.write("\x1b[0m")
        sys.stdout.flush()
        os.system("clear")
            
