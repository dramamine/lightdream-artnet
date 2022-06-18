import os
from util.track_metadata import tracks

from modules.audio_player import AudioPlayer
from modules.sequence_player import SequencePlayer
import random

# assume mode is sequences, at least for this file.

class Playlist:
  def __init__(self):
    self.queue = []
    self.idx = 0
    self.sp = SequencePlayer()
    self.ap = AudioPlayer()

    self.now_playing = None
    self.updates_cb = None
  
  # cb: this function gets called whenever there's an update to the
  # currently playing track or the queue. ex.:
  # (now_playing: str, queue: [str] ) where `str` is the track id
  def subscribe_to_playlist_updates(self, cb):
    self.updates_cb = cb

  def start(self):
    random.shuffle(tracks)
    self.start_track(self.pick_track())

  def stop(self):
    self.ap.stop()

  def __del__(self):
    self.stop()

  def pick_track(self):
    if self.queue:
      return self.queue.pop(0)
    
    self.idx = (self.idx+1) % len(tracks)
    return tracks[self.idx]
    
  def start_track(self, track_name):
    print("starting audio:", track_name)

    self.ap.play(os.path.join('audio', '{}.ogg'.format(track_name)))
    self.sp.play(os.path.join('video', 'sequences', '{}.mp4'.format(track_name)))

    self.now_playing = track_name
    self.queue_updated()


  def test_metronome(self):
    self.queue = []
    self.ap.clear()
    self.ap.play(os.path.join('audio', 'metronome.wav'))
    self.sp.play(os.path.join('video', 'metronome_clockwise_x264.mp4'))

  # check status of audio; return next LED frame from the sequence
  def tick(self):
    if not self.ap.is_playing():
      print("song ended.")
      self.start_track( self.pick_track() )
    
    return self.sp.read_frame()

  def enqueue(self, track_name):
    # assert(track_name in tracks)
    self.queue.append(track_name)
    self.queue_updated()

  def dequeue(self, track_name):
    self.queue.remove(track_name)
    self.queue_updated()

  def skip_track(self):
    self.ap.skip_track()
    self.start_track(self.pick_track())
    self.queue_updated()

  def queue_updated(self):
    if self.updates_cb != None:
      self.updates_cb(self.now_playing, self.queue)

  def clear(self):
    self.ap.clear()
