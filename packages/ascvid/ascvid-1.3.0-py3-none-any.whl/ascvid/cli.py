from .player import play_vid
from .run_terminal import run_term 
import click
import sys
@click.command()
@click.argument("file")
@click.option("--hide-cursor","-H",default=False,is_flag=True,help="Hide the cursor while playing the video")
@click.option("--no-audio","-A",is_flag=True,default=False,help="Don't play audio stream")
@click.option("--fps","-f",default=None,help="Number of FPS the video's supposed to run at. If None, it's determined from the video. If \"max\", ascvid will try its best to keep the video from lagging")
@click.option("--char","-c",default='\u2588',type=str,help="Character to be used while rendering the video frames")
@click.option("--no-color","-C",default=False,is_flag=True,help="Don't color output")
@click.option("--ascii","-a",is_flag=True,default=False,help="Use multiple ASCII characters. Best to be used with --no-truecolor")
@click.option("--no-truecolor","-T",is_flag=True,default=False,help="Reduces color palette. Use this flag on more stupid terminals (windows).")
@click.option("--fast","-F",is_flag=True,default=False,help="Toggles off resizing each frame individually, rather resizes the entire video. Use this if the video is lagging too much.")
@click.option("--disable-controls","-d",is_flag=True,default=False,help="Disables pausing the video")
@click.option("--title","-t",default=None,help="Sets the title of the video. If not set, file name will be used instead")
@click.option("--hide-title","-h",default=False,is_flag=True,help="hides the title")
@click.option("--new-window","-n",is_flag=True,help="Opens in a new terminal window")
@click.option("--term","-t",default=None,help="Specify terminal in format '<terminal command> <run command switch> {}'")
@click.option("--outfile","-o",default=None,help="Specify output file")
def main(file,hide_cursor,no_audio,fps,char,no_color,ascii,no_truecolor,fast,disable_controls,title,hide_title,new_window,term,outfile):
    if new_window:
        cmd = [sys.executable,"-m","ascvid",file]
        if hide_cursor:
            cmd.extend(["-H"])
        if no_audio:
            cmd.extend(["-A"])
        if fps is not None:
            cmd.extend(["-f"])
            cmd.extend([f"{fps}"])
        cmd.extend(["-c",f"{char}"])
        if no_color:
            cmd.extend(["-C"])
        if ascii:
            cmd.extend(["-a"])
        if no_truecolor:
            cmd.extend(["-T"])
        if fast:
            cmd.extend(["-F"])
        if disable_controls:
            cmd.extend(["-d"])
        if title is not None:
            cmd.extend(["-t",f"{title}"])
        if hide_title:
            cmd.extend(["-h"])
        run_term(' '.join(cmd),term)
        return
    if fps and fps!="max":
        fps=int(fps)
    play_audio=not no_audio
    colored = not no_color
    truecolor = not no_truecolor
    play_vid(file,hide_cursor,play_audio,fps,char,colored,truecolor,ascii,fast,disable_controls,title,not hide_title,outfile)
