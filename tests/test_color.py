from pynextion.color import (
    NamedColor,
    Color
)


def test_named_color():
    assert NamedColor.BLACK.value == 0
    assert NamedColor.WHITE.value == 65535
    assert NamedColor.RED.value == 63488
    assert NamedColor.GREEN.value == 2016
    assert NamedColor.BLUE.value == 31
    assert NamedColor.GRAY.value == 33840
    assert NamedColor.BROWN.value == 48192
    assert NamedColor.YELLOW.value == 65504


def test_color_from_name():
    assert NamedColor.from_string("RED").value == 63488


def test_color():
    (r, g, b) = (0, 0, 0)  # black
    color = Color(r, g, b)
    assert color.value == 0

    (r, g, b) = ((1 << 5) - 1, (1 << 6) - 1, (1 << 5) - 1)  # white
    color = Color(r, g, b)
    assert color.value == (1 << 16) - 1  # 65535


def test_color_from_float():
    (r, g, b) = (0.0, 0.0, 0.0)  # black
    color = Color.from_float(r, g, b)
    assert color.value == 0
    assert color.to_tuple() == (0, 0, 0)

    (r, g, b) = (0.0, 0.0, 1.0)  # blue
    color = Color.from_float(r, g, b)
    assert color.value == (1 << 5) - 1  # 31
    assert color.to_tuple() == (0, 0, 31)

    (r, g, b) = (0.0, 1.0, 0.0)  # green
    color = Color.from_float(r, g, b)
    assert color.value == 2016
    assert color.to_tuple() == (0, 63, 0)

    (r, g, b) = (1.0, 0.0, 0.0)  # red
    color = Color.from_float(r, g, b)
    assert color.value == 63488
    assert color.to_tuple() == (31, 0, 0)

    (r, g, b) = (1.0, 1.0, 1.0)  # white
    color = Color.from_float(r, g, b)
    assert color.value == 65535
    assert color.to_tuple() == (31, 63, 31)


def test_other_colors():
    (r, g, b) = (1 << 4, (1 << 5) + 1, 1 << 4)  # gray
    # (r, g, b) = (16, 33, 16)
    color = Color(r, g, b)
    assert color.value == 33840

    (r, g, b) = (23, 34, 0)  # brown
    color = Color(r, g, b)
    assert color.value == 48192

    (r, g, b) = ((1 << 5) - 1, (1 << 6) - 1, 0)  # yellow
    # (r, g, b) = (31, 63, 0)
    color = Color(r, g, b)
    assert color.value == 65504
