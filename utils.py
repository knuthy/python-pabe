__author__ = 'knuthy'


def uniquify(seq):
    return list(_f7(seq))


def _f7(seq):
    seen = set()
    for x in seq:
        if x in seen:
            continue
        seen.add(x)
        yield x

  