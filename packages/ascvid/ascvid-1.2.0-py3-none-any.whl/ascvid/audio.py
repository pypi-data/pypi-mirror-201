import sounddevice as sd
import time
import moviepy.editor as mp
from .timer import Timer
class Audio:
    def __init__(self,clip):
        self.clip=clip
        self.audio=clip.audio.to_soundarray()
        self.fps=clip.audio.fps
        self.start_time=-1
        self.resume_time=0
        self._playing=False
        self.timer=Timer()
    def play(self):
        self.timer.start()
        sd.play(self.audio,self.fps)
    @property
    def playing(self):
        if not self._playing:
            return False
        return self._playing and (not sd.get_stream().stopped)
    def pause(self):
        self.timer.pause()
        self._playing=False
        sd.stop()
    def resume(self):
        
        a=self.audio[int(self.fps*self.timer.curtime):]        
        self.timer.start()
        sd.play(a,self.fps)

    
