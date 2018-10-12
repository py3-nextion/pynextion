from .constants import (
    Background,
    Colour,
    Alignment,
    BACKCOLOR_DEFAULT,
    FORECOLOR_DEFAULT
)
from .resources import FONT_DEFAULT
from .int_tools import assert_integers_in_range


def _init_colour(colour):
    if colour is None:
        return Colour.NONE.value
    else:
        return colour.value


def cls(nexSerial, colour=None):
    """
    Clear screen (CLear Screen).

    `colour` can be:

    - a string
    - a decimal value
    - a `Colour` enum

    :Usage:

    >>> from pynextion.draw import cls
    >>> cls(nexSerial)
    """
    colour = _init_colour(colour)
    return nexSerial.send("cls %s" % colour)


def rectangle(nexSerial, x1, y1, x2, y2, colour=None, mode=Background.NOBACKCOLOUR):
    """
    Draw a rectangle, the top left coordinate is (x1, y1)
    and bottom right corner is (x2, y2)

    If `mode` is not set (or set `NOBACKCOLOUR`)
    `colour` is used for frame colour.

    If `mode` is set to `SOLIDCOLOUR`
    `colour` is used for fill colour.
    """
    assert_integers_in_range((x1, y1, x2, y2), False, 16)  # uint16
    colour = _init_colour(colour)
    if mode == Background.NOBACKCOLOUR:
        return nexSerial.send("draw %s,%s,%s,%s,%s" % (x1, y1, x2, y2, colour))
    elif mode == Background.SOLIDCOLOUR:
        w = x2 - x1
        h = y2 - y1
        return nexSerial.send("fill %s,%s,%s,%s,%s" % (x1, y1, w, h, colour))
    else:
        raise(Exception("Unsupported $mode"))


def circle(nexSerial, x, y, r, colour=None, mode=Background.NOBACKCOLOUR):
    """
    Draw a hollow circle whose radius is `r` with the coordinate (`x`, `y`)
    as the center of a circle.

    If `mode` is not set (or set `NOBACKCOLOUR`)
    `colour` is used for circle frame line.

    If `mode` is set to `SOLIDCOLOUR`
    `colour` is used for fill colour.
    """
    assert_integers_in_range((x, y, r), False, 16)  # uint16
    colour = _init_colour(colour)
    if mode == Background.NOBACKCOLOUR:
        return nexSerial.send("cir %s,%s,%s,%s" % (x, y, r, colour))
    elif mode == Background.SOLIDCOLOUR:
        return nexSerial.send("cirs %s,%s,%s,%s" % (x, y, r, colour))
    else:
        raise(Exception("Unsupported $mode"))


def xstr(nexSerial, s, x, y, w, h,
         font=FONT_DEFAULT, fontcolor=FORECOLOR_DEFAULT, backcolor=BACKCOLOR_DEFAULT,
         xcenter=Alignment.Horizontal.LEFT,
         ycenter=Alignment.Vertical.UP,
         sta=Background.SOLIDCOLOUR):
    """
    Print string on the device.

    - `s`: Character content
    - `x`: x coordinate starting point;
    - `y`: y coordinate starting point;
    - `w`: area width;
    - `h`: area height;
    - `font`: Font resource (should have a id attribute)
    - `fontcolor`: Font color;
    - `backcolor`: Background color (when set sta as Crop Image or Image, backcolor means image ID );
    - `xcenter`: Horizontal alignment (0 is left-aligned, 1 is centered, 2 is right-aligned);
    - `ycenter`: Vertical alignment (0 is upper-aligned, 1 is centered, 2 is lower-aligned);
    - `sta`: Background fill(0-crop image;1-solid color;2-Image; 3-No backcolor, when set sta as Crop Image or Image, backcolor means image ID);
    """
    assert_integers_in_range((x, y, w, h), False, 16)  # uint16
    fontid = font.id
    xcenter = xcenter.value
    ycenter = ycenter.value
    sta = sta.value
    return nexSerial.send("xstr %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,\"%s\"" % (x, y, w, h, fontid, fontcolor, backcolor, xcenter, ycenter, sta, s))


def line(nexSerial, x1, y1, x2, y2, colour=None):
    """
    Draw a line in colour `colour` between
    the coordinate (`x1`, `y1`) and the coordinate (`x2`, `y2`)
    """
    assert_integers_in_range((x1, y1, x2, y2), False, 16)  # uint16
    colour = _init_colour(colour)
    return nexSerial.send("line %s,%s,%s,%s,%s" % (x1, y1, x2, y2, colour))


def picture(nexSerial, x, y, pic, w=None, h=None, x0=None, y0=None):
    """
    Display the Picture pic (should have a id attribute) in resource file
    at the coordinate (`x`, `y`)
    """
    assert_integers_in_range((x, y), False, 16)  # uint16
    picid = pic.id
    if w is None and x0 is None:
        return nexSerial.send("pic %s,%s,%s" % (x, y, picid))
    elif x0 is None:
        return nexSerial.send("picq %s,%s,%s,%s,%s" % (x, y, w, h, picid))
    else:
        return nexSerial.send("xpic %s,%s,%s,%s,%s,%s,%s" % (x, y, w, h, x0, y0, picid))  # xpic or picq?
