
deb = True


def debug(inf, /, end="\n"):
    """
    Prints info if variable deb is True
    :param inf: info to print
    """
    if deb:
        print(inf, end=end)


def range_cut(mi, ma, val):
    """
    Cuts value from min to max
    :param mi: minimum value
    :param ma: maximum value
    :param val: value
    :return: cut value
    """
    return min(ma, max(mi, val))
