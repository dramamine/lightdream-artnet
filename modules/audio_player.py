import pyglet

player = pyglet.media.Player()

class AudioPlayer:
  def play(self, path):
    source = pyglet.media.load(path)
    player.queue(source)
    player.play()

  def is_playing(self):
    # lol side effects - necessary since we're not in a pyglet app
    pyglet.clock.tick()
    pyglet.app.platform_event_loop.dispatch_posted_events()
    
    return player.playing

  # @TODO needs testing
  def stop(self):
    player.delete()
