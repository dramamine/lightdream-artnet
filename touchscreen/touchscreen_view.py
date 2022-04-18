# importing pyglet module
import pyglet

SCALE_FACTOR = 0.5

# width of window
width = 2405 * SCALE_FACTOR

# height of window
height = 1367 * SCALE_FACTOR

# creating a window
window = pyglet.window.Window(width, height, 'lightdream')

# render the layout
image = pyglet.image.load('../images/!touchscreen layout 3.png')
sprite = pyglet.sprite.Sprite(image, x=0, y=0)
sprite.scale = SCALE_FACTOR

# on draw event
@window.event
def on_draw():

    # clear the window
    window.clear()

    # draw the image on screen
    sprite.draw()

# start running the application
pyglet.app.run()