import os
from collections import deque
from queue import Queue
from util.track_metadata import tracks

from modules.audio_player import AudioPlayer
from modules.sequence_player import SequencePlayer
import random

# assume mode is sequences, at least for this file.

class Playlist:
  def __init__(self):
    self.deque = deque()
    self.idx = 0
    self.sp = SequencePlayer()
    self.ap = AudioPlayer()

    self.now_playing = None
    self.updates_cb = None

    self.dirty = Queue()

  def start(self):
    random.shuffle(tracks)
    self.start_track(self.pick_track())

  def stop(self):
    self.ap.stop()

  def __del__(self):
    self.stop()

  def pick_track(self):
    if len(self.deque) > 0:
      return self.deque.popleft()
    
    self.idx = (self.idx+1) % len(tracks)
    return tracks[self.idx]
    
  def start_track(self, track_name):
    self.ap.load(track_name)
    self.ap.play(track_name)
    self.sp.play(os.path.join('video', 'sequences', '{}.mp4'.format(track_name)))

    self.now_playing = track_name
    self.deque_updated()


  def test_metronome(self):
    self.deque.clear()
    self.sp.play(os.path.join('video', 'metronome_clockwise_x264.mp4'))
    self.ap.clear()
    self.ap.play('metronome')

  # check status of audio; return next LED frame from the sequence
  def tick(self):
    if not self.ap.is_playing():
      print("song ended.")
      self.start_track( self.pick_track() )
    
    return self.sp.read_frame()

  def needs_to_load_audio(self):
    return not self.ap.is_playing()

  def enqueue(self, track_name):
    # no duplicates; could just be too many presses from kivy
    try:
      x = self.deque.index(track_name)
    except ValueError:
      self.deque.append(track_name)
      self.deque_updated()


  def dequeue(self, track_name):
    try:
      self.deque.remove(track_name)
      self.deque_updated()
    except ValueError:
      # track wasn't in list, but lets just ignore it
      pass

  def skip_track(self):
    self.ap.skip_track()
    self.start_track(self.pick_track())
    self.deque_updated()

  def deque_updated(self):
    self.dirty.put(1, block=True, timeout=5)

  def clear(self):
    self.ap.clear()
