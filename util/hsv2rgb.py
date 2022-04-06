import math

def hsv2rgb(h, s, v):
    
    """HSV to RGB
    
    :param float h: 0.0 - 360.0
    :param float s: 0.0 - 1.0
    :param float v: 0.0 - 1.0
    :return: rgb 
    :rtype: list
    
    """
    
    c = v * s
    x = c * (1 - abs(((h/60.0) % 2) - 1))
    m = v - c
    
    if 0.0 <= h < 60:
        rgb = (c, x, 0)
    elif 0.0 <= h < 120:
        rgb = (x, c, 0)
    elif 0.0 <= h < 180:
        rgb = (0, c, x)
    elif 0.0 <= h < 240:
        rgb = (0, x, c)
    elif 0.0 <= h < 300:
        rgb = (x, 0, c)
    elif 0.0 <= h < 360:
        rgb = (c, 0, x)
        
    return list(map(lambda n: (n + m) * 255, rgb))
