from PIL import Image
from math import sqrt
import moviepy.editor as mp
import sys
import os
import time
import cursor
import threading
import getkey
import queue
from .getcol import closest_color
from .logger import print_error,print_warning
from . import audio
CHARS = ' .\'`^",:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$\u2591\u2592\u2593\u2588'
CLOSEST_CACHE = {}
CHAR_CACHE = {}
def fqget(q):
    if q.empty():
        return
    return q.get()
def _getchar(color):
    if color in CHAR_CACHE:
        return CHAR_CACHE[color]
    brightness=round(get_brightness(color))
    charindex=int((brightness/255)*(len(CHARS)-1))
    char=CHARS[charindex]
    CHAR_CACHE[color]=char
    return char

def check_paused(q):
    def check():
        while True:
            q.put(getkey.getkey())
    return check
def closest(col):
    global CLOSEST_CACHE
    if col in CLOSEST_CACHE:
        return CLOSEST_CACHE[col]
    cl=closest_color(col)
    CLOSEST_CACHE[col]=cl
    return cl
def clear(out):
    out.write("\x1b[H\x1b[2J\x1b[3J")
def get_brightness(col):
    R,G,B=col
    return sqrt(0.299 * R**2 + 0.587 * G**2 + 0.114 * B**2)

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

def show_frame(fr,char,colored,truecolor,use_ascii,resize,hast,tit,out):
    ts=os.get_terminal_size()
    tw=ts.columns
    th=ts.lines
    if hast:
        th-=1
    out.write('\033[H')
    out.flush()
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
    clear(out)
    if hast:
        print(tit,file=out)
    print('\n'.join(lines),end="",file=out)
def mkpos(a):
    if a<0:
        return 0
    return a
def play_vid(file,hide_cursor=True,play_audio=True,fps=None,char="\u2588",colored=True,truecolor=True,use_ascii=False,fast=False,disable_controls=False,title=None,show_title=True,out=None):
    if out is None:
        out=sys.stdout
    else:
        out=open(out,"w")
    if title is None:
        title=file

    vid=mp.VideoFileClip(file)
    q=queue.Queue()
    settings=None
    if sys.platform.lower().startswith("linux"):
        import tty
        import termios
        settings=termios.tcgetattr(sys.stdin)

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
    audio_stream=None
    if hide_cursor:
        cursor.hide()
    if play_audio and vid.audio is not None:
        audio_stream=audio.Audio(vid)
        audio_stream.play()
    if not disable_controls:
        check_thread=threading.Thread(target=check_paused(q),daemon=True)
        check_thread.start()
    clear(out)
    try: 
        for frame in vid.iter_frames():

            if not disable_controls:
                resp=fqget(q)
                if resp==" ":
                    if audio_stream is not None:
                        audio_stream.pause()
                    while q.get()!=" ":
                        pass
                    if audio_stream is not None:
                        audio_stream.resume()
            t=time.time()
            show_frame(frame,char,colored,truecolor,use_ascii,not fast,show_title,title,out)
            if fps!="max":
                time.sleep(mkpos(1/fps-(time.time()-t)))
    finally:
        cursor.show()
        out.write("\x1b[0m")
        out.flush()
        if settings is not None:
            time.sleep(0.2)
            termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, settings)

        clear(out)

           

