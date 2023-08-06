from .player import play_vid
import click

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
def main(file,hide_cursor,no_audio,fps,char,no_color,ascii,no_truecolor,fast):
    if fps and fps!="max":
        fps=int(fps)
    play_audio=not no_audio
    colored = not no_color
    truecolor = not no_truecolor
    play_vid(file,hide_cursor,play_audio,fps,char,colored,truecolor,ascii,fast)
