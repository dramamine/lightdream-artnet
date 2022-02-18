import pyglet
from time import sleep

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


# if __name__ == "__main__":
#   source = pyglet.media.load('.\\audio\\1s.ogg')
#   player.queue(source)
#   player.play()
#   while(True):
#     sleep(1)
#     pyglet.clock.tick()
#     pyglet.app.platform_event_loop.dispatch_posted_events()

#     if player.playing == False:
#       print("ended")
