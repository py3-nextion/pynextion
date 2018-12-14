class Color:
    def __init__(self, r=None, g=None, b=None):
        if r is None and g is None and b is None:
            self.defined = False
        else:
            assert isinstance(r, int)
            assert r >= 0 and r < (1 << 5)
            self.r = r

            assert isinstance(g, int)
            assert g >= 0 and g < (1 << 6)
            self.g = g

            assert isinstance(b, int)
            assert b >= 0 and b < (1 << 5)
            self.b = b

            self.defined = True

    @classmethod
    def from_float(cls, r, g, b):
        assert r >= 0 and r <= 1
        assert g >= 0 and g <= 1
        assert b >= 0 and b <= 1
        r = int(r * ((1 << 5) - 1))
        g = int(g * ((1 << 6) - 1))
        b = int(b * ((1 << 5) - 1))
        return cls(r, g, b)

    @property
    def value(self):
        if self.defined:
            return self.b + (self.g << 5) + (self.r << 11)
        else:
            return -1

    def to_tuple(self):
        return (self.r, self.g, self.b)


class NamedColor:
    NONE = Color()  # -1
    BLACK = Color(0, 0, 0)  # 0
    WHITE = Color(31, 63, 31)  # 65535
    RED = Color(31, 0, 0)  # 63488
    GREEN = Color(0, 63, 0)  # 2016
    BLUE = Color(0, 0, 31)  # 31
    GRAY = Color(16, 33, 16)  # 33840
    BROWN = Color(23, 34, 0)  # 48192
    YELLOW = Color(31, 63, 0)  # 65504

    @classmethod
    def from_string(cls, s):
        return cls.__dict__[s]


BACKCOLOR_DEFAULT = NamedColor.WHITE
FORECOLOR_DEFAULT = NamedColor.BLACK
