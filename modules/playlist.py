from ctypes import sizeof
from email.mime import audio
import os


from modules.audio_player import AudioPlayer
from modules.sequence_player import SequencePlayer
import random

# assume mode is sequences, at least for this file.

song_options = ['asineedyou', 'dyscontrolled', 'misty', 'moses']

class Playlist:
  def __init__(self):
    self.queue = []
    self.sp = SequencePlayer()
    self.ap = AudioPlayer()

  def restart(self):
    self.start_track(self.pick_track())

  def __del__(self):
    self.ap.stop()

  def pick_track(self):
    if self.queue:
      return self.queue.pop(0)
    
    return random.choice(song_options)
    
  def start_track(self, track_name):
    print("hello from start track:", track_name)

    self.ap.play(os.path.join('audio', '{}.ogg'.format(track_name)))
    self.sp.play(os.path.join('video', '{}.mp4'.format(track_name)))

  def test_metronome(self):
    self.ap.play(os.path.join('audio', 'metronome.wav'))
    self.sp.play(os.path.join('video', 'metronome_clockwise_x264.mp4'))

  # check status of audio; return next LED frame from the sequence
  def tick(self):
    if not self.ap.is_playing():
      self.start_track( self.pick_track() )
    
    return self.sp.read_frames()
