def limits(signed, bit_size):
    signed_limit = 2 ** (bit_size - 1)
    return (-signed_limit, signed_limit - 1) if signed else (0, 2 * signed_limit - 1)


def str_int(signed, bit_size):
    s = "u" if not signed else ""
    s += "int"
    s += "%s" % bit_size
    return s


def assert_int_in_range(value, signed, bit_size):
    min_val, max_val = limits(signed, bit_size)
    if value < min_val or value > max_val:
        s_typ = str_int(signed, bit_size)
        lim = limits(signed, bit_size)
        raise(ValueError("%d not in range of %s %s" % (value, s_typ, lim)))


def assert_integers_in_range(values, signed, bit_size):
    for value in values:
        assert_int_in_range(value, signed, bit_size)
