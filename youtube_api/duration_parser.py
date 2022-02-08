import datetime


def _get_isosplit(s, split):
    if split in s:
        n, s = s.split(split)
    else:
        n = 0
    return n, s


def parse_isoduration(s):
    # Remove prefix
    s = s.split('P')[-1]

    # Step through letter dividers
    days, s = _get_isosplit(s, 'D')
    _, s = _get_isosplit(s, 'T')
    hours, s = _get_isosplit(s, 'H')
    minutes, s = _get_isosplit(s, 'M')
    seconds, s = _get_isosplit(s, 'S')

    # Convert all to seconds
    dt = datetime.timedelta(days=int(days), hours=int(hours), minutes=int(minutes), seconds=int(seconds))
    return int(dt.total_seconds())
