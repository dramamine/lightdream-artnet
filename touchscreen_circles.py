from effects.filters import FilterNames


class TouchscreenCircle:
    """
    TouchscreenCircle Assumptions

     - uses SCALED coordinates to position each circle in the layout
     - each image path is for the inactive image; for xyz.png, assume xyz-active.png exists

    full_image_radius:

     - this is the radius, in SCALED pixels, of each circle when it is displayed
       at its file-size width.
     - to adjust the fit between touch-target and image, adjust full_image_radius.

    """
    def __init__(self, name='', path='', key='', center=None, radius=0, full_image_radius=0):
        self.name = name
        self.path = path
        self.key = key
        self.center = center
        self.radius = radius
        self.full_image_radius = full_image_radius

    # we can use this to place the image sprites
    def lower_left_corner(self):
        x = self.center[0] - self.radius
        y = self.center[1] - self.radius
        return (x, y)

    @property
    def X(self):
        return self.lower_left_corner()[0]

    @property
    def Y(self):
        return self.lower_left_corner()[1]

    @property
    def SCALE(self):
        return self.radius / self.full_image_radius


# LEFT bigger circles
HUESHIFT = TouchscreenCircle(
    path='./images/colorwheel-dithered.png',
    key=FilterNames.HUESHIFT,
    name='HUESHIFT',
    center=(250, 545),
    radius=210,
    full_image_radius=800
)
KALEIDOSCOPE = TouchscreenCircle(
    path='./images/kaleidoscope.png',
    key=FilterNames.KALEIDOSCOPE,
    name='KALEIDOSCOPE',
    center=(681, 812),
    radius=210,
    full_image_radius=800
)
TUNNEL = TouchscreenCircle(
    path='./images/tunnel.png',
    key=FilterNames.TUNNEL,
    name='TUNNEL',
    center=(677, 228),
    radius=210,
    full_image_radius=800
)
# LEFT smaller circles
LIGHTNING = TouchscreenCircle(
    path='./images/lightning.png',
    key=FilterNames.LIGHTNING,
    name='LIGHTNING',
    center=(333, 114),
    radius=80,
    full_image_radius=500
)
NUCLEAR = TouchscreenCircle(
    path='./images/nuclear.png',
    key=FilterNames.NUCLEAR,
    name='NUCLEAR',
    center=(130, 206),
    radius=80,
    full_image_radius=500
)
SPIRAL = TouchscreenCircle(
    path='./images/spiral.png',
    key=FilterNames.SPIRAL,
    name='SPIRAL',
    center=(1549, 965),
    radius=80,
    full_image_radius=500
)
RADIANTLINES = TouchscreenCircle(
    path='./images/radiant-lines.png',
    key=FilterNames.RADIANTLINES,
    name='RADIANTLINES',
    center=(1751, 873),
    radius=80,
    full_image_radius=500
)

