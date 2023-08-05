# This file is placed in the Public Domain.
# pylint: disable=C0116


'utilities'


import os


def __dir__():
    return (
            'elapsed',
            'fnclass',
            'spl'
           )


__all__ = __dir__()


def elapsed(seconds, short=True):
    txt = ""
    nsec = float(seconds)
    if nsec < 1:
        return f"{nsec:.2f}s"
    year = 365*24*60*60
    week = 7*24*60*60
    nday = 24*60*60
    hour = 60*60
    minute = 60
    years = int(nsec/year)
    nsec -= years*year
    weeks = int(nsec/week)
    nsec -= weeks*week
    nrdays = int(nsec/nday)
    nsec -= nrdays*nday
    hours = int(nsec/hour)
    nsec -= hours*hour
    minutes = int(nsec/minute)
    nsec -= int(minute*minutes)
    sec = int(nsec)
    if years:
        txt += "%sy" % years
    if weeks:
        nrdays += weeks * 7
    if nrdays:
        txt += "%sd" % nrdays
    if years and short and txt:
        return txt.strip()
    if hours:
        txt += "%sh" % hours
    if minutes:
        txt += "%sm" % minutes
    if sec:
        txt += "%ss" % sec
    txt = txt.strip()
    return txt


def fnclass(pth):
    try:
        _rest, *path2 = pth.split('store')
        splitted = path2[0].split(os.sep)
        return splitted[1]
    except (ValueError, IndexError):
        return pth.split(os.sep)[0]
    return None


def spl(txt):
    try:
        res = txt.split(',')
    except (TypeError, ValueError):
        res = txt
    return [x for x in res if x]
