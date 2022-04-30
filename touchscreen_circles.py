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
    def __init__(self, path='', key='', center=None, radius=0, full_image_radius=0):
        self.path = path
        self.key = key
        self.center = center
        self.radius = radius
        self.full_image_radius = full_image_radius

    # we can use this to place the image sprites
    def lower_right_corner(self):
        x = self.center[0] - self.radius
        y = self.center[1] - self.radius
        return (x, y)

    @property
    def X(self):
        return self.lower_right_corner()[0]

    @property
    def Y(self):
        return self.lower_right_corner()[1]

    @property
    def SCALE(self):
        return self.radius / self.full_image_radius


# LEFT bigger circles
HUESHIFT = TouchscreenCircle(
    path='./images/colorwheel-dithered.png',
    key=FilterNames.HUESHIFT,
    center=(312, 683),
    radius=262,
    full_image_radius=800
)
KALEIDOSCOPE = TouchscreenCircle(
    path='./images/kaleidoscope.png',
    key=FilterNames.KALEIDOSCOPE,
    center=(850, 1015),
    radius=262,
    full_image_radius=800
)
TUNNEL = TouchscreenCircle(
    path='./images/tunnel.png',
    key=FilterNames.TUNNEL,
    center=(850, 288),
    radius=262,
    full_image_radius=800
)
# LEFT smaller circles
LIGHTNING = TouchscreenCircle(
    path='./images/lightning.png',
    key=FilterNames.LIGHTNING,
    center=(414, 146),
    radius=106,
    full_image_radius=500
)
NUCLEAR = TouchscreenCircle(
    path='./images/nuclear.png',
    key=FilterNames.NUCLEAR,
    center=(166, 260),
    radius=106,
    full_image_radius=500
)
SPIRAL = TouchscreenCircle(
    path='./images/spiral.png',
    key=FilterNames.SPIRAL,
    center=(160, 1095),
    radius=106,
    full_image_radius=500
)
RADIANTLINES = TouchscreenCircle(
    path='./images/radiant-lines.png',
    key=FilterNames.RADIANTLINES,
    center=(416, 1205),
    radius=106,
    full_image_radius=500
)

