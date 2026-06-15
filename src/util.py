def formatTime(seconds:int):
    m, s = divmod(seconds, 60)
    if m <= 60:
        return f'{m}:{s:02d}'
    h, m = divmod(m, 60)
    return f'{h}:{m:02d}:{s:02d}'


def progressBar(progress:float, totalChar:int):
    placement = progress * totalChar
    string = ''
    for i in range(int(placement)):
        string += "-"

    string += "|"
    for i in range(int(placement), totalChar):
        string += "-"

    return string



