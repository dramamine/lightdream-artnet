from effects.filters import FilterNames


class TouchscreenCircle:
    """
    TouchscreenCircle Assumptions
     - each image path is for the inactive image; for img.png, assume img-active.png exists
    """
    def __init__(self, path='', key='', center=None, radius=0):
        self.path = path
        self.key = key
        self.center = center
        self.radius = radius

    @property
    def X(self):
        return self.lower_left_corner()[0]

    @property
    def Y(self):
        return self.lower_left_corner()[1]

    @property
    def active_path(self):
        return self.path.replace('.png', '-active.png')


HUESHIFT = TouchscreenCircle(
    path='./images/colorwheel-dithered.png',
    key=FilterNames.HUESHIFT,
    center=(250, 545),
    radius=205,
)
KALEIDOSCOPE = TouchscreenCircle(
    path='./images/kaleidoscope.png',
    key=FilterNames.KALEIDOSCOPE,
    center=(681, 812),
    radius=205,
)
TUNNEL = TouchscreenCircle(
    path='./images/tunnel.png',
    key=FilterNames.TUNNEL,
    center=(677, 228),
    radius=205,
)
LIGHTNING = TouchscreenCircle(
    path='./images/lightning.png',
    key=FilterNames.LIGHTNING,
    center=(333, 114),
    radius=80,
)
NUCLEAR = TouchscreenCircle(
    path='./images/nuclear.png',
    key=FilterNames.NUCLEAR,
    center=(130, 206),
    radius=80,
)
SPIRAL = TouchscreenCircle(
    path='./images/spiral.png',
    key=FilterNames.SPIRAL,
    center=(1549, 965),
    radius=80,
)
RADIANTLINES = TouchscreenCircle(
    path='./images/radiant-lines.png',
    key=FilterNames.RADIANTLINES,
    center=(1751, 873),
    radius=80,
)
RINGS = TouchscreenCircle(
    path='./images/rings.png',
    key=FilterNames.RINGS,
    center=(1196, 811),
    radius=225,
)
SPOTLIGHT = TouchscreenCircle(
    path='./images/spotlight.png',
    key=FilterNames.SPOTLIGHT,
    center=(1655, 545),
    radius=200,
)
WEDGES = TouchscreenCircle(
    path='./images/wedges.png',
    key=FilterNames.WEDGES,
    center=(1196, 229),
    radius=225,
)
TRIFORCE = TouchscreenCircle(
    path='./images/triforce.png',
    key=FilterNames.TRIFORCE,
    center=(1752, 195),
    radius=80,
)
BLOBS = TouchscreenCircle(
    path='./images/blobs.png',
    key=FilterNames.BLOBS,
    center=(1551, 113),
    radius=80,
)
