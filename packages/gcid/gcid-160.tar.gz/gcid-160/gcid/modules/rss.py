# This file is placed in the Public Domain.
# pylint: disable=C0115,C0116,R0903,E1101,E0402


'rich site syndicate'


import html.parser
import re
import threading
import time
import urllib
import _thread


from urllib.error import HTTPError, URLError
from urllib.parse import quote_plus, urlencode
from urllib.request import Request, urlopen


from ..clocked import Repeater
from ..handler import Listens
from ..objects import Object, printable, update
from ..persist import find, fntime, last, write
from ..threads import launch, threaded


from .utility import elapsed, spl


def __dir__():
    return (
        'Feed',
        'Fetcher',
        'Repeater',
        'Rss',
        'Seen',
        'Timer',
        'debug',
        'dpl',
        'ftc',
        'nme',
        'rem',
        'rss',
        'start'
    )


def start():
    fetcher = Fetcher()
    fetcher.start()
    return fetcher


DEBUG = False
fetchlock = _thread.allocate_lock()


class Feed(Object):

    pass


class Rss(Object):

    def __init__(self):
        super().__init__()
        self.display_list = 'title,link,author'
        self.name = ''
        self.rss = ''


class Seen(Object):

    def __init__(self):
        super().__init__()
        self.urls = []


class Fetcher(Object):

    dosave = False
    seen = Seen()

    def __init__(self):
        super().__init__()
        self.connected = threading.Event()

    def clone(self, other):
        pass

    @staticmethod
    def display(obj):
        result = ''
        displaylist = []
        try:
            displaylist = obj.display_list or 'title,link'
        except AttributeError:
            displaylist = 'title,link,author'
        for key in spl(displaylist):
            if not key:
                continue
            data = getattr(obj, key, None)
            if not data:
                continue
            data = data.replace('\n', ' ')
            data = striphtml(data.rstrip())
            data = unescape(data)
            result += data.rstrip()
            result += ' - '
        return result[:-2].rstrip()

    def fetch(self, feed):
        with fetchlock:
            counter = 0
            objs = []
            for obj in reversed(list(getfeed(feed.rss, feed.display_list))):
                fed = Feed()
                update(fed, obj)
                update(fed, feed)
                if 'link' in fed:
                    url = urllib.parse.urlparse(fed.link)
                    if url.path and not url.path == '/':
                        uurl = '%s://%s/%s' % (
                                               url.scheme,
                                               url.netloc,
                                               url.path
                                              )
                    else:
                        uurl = fed.link
                    if uurl in Fetcher.seen.urls:
                        continue
                    Fetcher.seen.urls.append(uurl)
                counter += 1
                if self.dosave:
                    write(fed)
                objs.append(fed)
        if objs:
            write(Fetcher.seen)
        txt = ''
        feedname = getattr(feed, 'name')
        if feedname:
            txt = '[%s] ' % feedname
        for obj in objs:
            txt2 = txt + self.display(obj)
            Listens.announce(txt2.rstrip())
        return counter

    def run(self):
        thrs = []
        for feed in find('rss'):
            thrs.append(launch(self.fetch, feed))
        return thrs

    def start(self, repeat=True):
        last(Fetcher.seen)
        if repeat:
            repeater = Repeater(300.0, self.run)
            repeater.start()


class Parser(Object):

    @staticmethod
    def getitem(line, item):
        lne = ''
        try:
            index1 = line.index('<%s>' % item) + len(item) + 2
            index2 = line.index('</%s>' % item)
            lne = line[index1:index2]
            if 'CDATA' in lne:
                lne = lne.replace('![CDATA[', '')
                lne = lne.replace(']]', '')
                lne = lne[1:-1]
        except ValueError:
            lne = None
        return lne


    @staticmethod
    def parse(txt, item='title,link'):
        res = []
        for line in txt.split('<item>'):
            line = line.strip()
            obj = Object()
            for itm in spl(item):
                setattr(obj, itm, Parser.getitem(line, itm))
            res.append(obj)
        return res


def getfeed(url, item):
    if DEBUG:
        return [Object(), Object()]
    try:
        result = geturl(url)
    except (ValueError, HTTPError, URLError):
        return [Object(), Object()]
    if not result:
        return [Object(), Object()]
    return Parser.parse(str(result.data, 'utf-8'), item)


def gettinyurl(url):
    postarray = [
        ('submit', 'submit'),
        ('url', url),
    ]
    postdata = urlencode(postarray, quote_via=quote_plus)
    req = Request('http://tinyurl.com/create.php',
                  data=bytes(postdata, 'UTF-8'))
    req.add_header('User-agent', useragent(url))
    for txt in urlopen(req).readlines():
        line = txt.decode('UTF-8').strip()
        i = re.search('data-clipboard-text="(.*?)"', line, re.M)
        if i:
            return i.groups()
    return []


def geturl(url):
    url = urllib.parse.urlunparse(urllib.parse.urlparse(url))
    req = urllib.request.Request(url)
    req.add_header('User-agent', useragent('OPB - object programming bot'))
    response = urllib.request.urlopen(req)
    response.data = response.read()
    return response


def striphtml(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


def unescape(text):
    txt = re.sub(r'\s+', ' ', text)
    return html.unescape(txt)


def useragent(txt):
    return 'Mozilla/5.0 (X11; Linux x86_64) ' + txt


def dpl(event):
    if len(event.args) < 2:
        event.reply('dpl <stringinurl> <item1,item2>')
        return
    setter = {'display_list': event.args[1]}
    for feed in find('rss', {'rss': event.args[0]}):
        if feed:
            update(feed, setter)
            write(feed)
    event.reply('ok')


@threaded
def ftc(event):
    res = []
    thrs = []
    fetcher = Fetcher()
    fetcher.start(False)
    thrs = fetcher.run()
    for thr in thrs:
        res.append(thr.join())
    if res:
        event.reply(','.join([str(x) for x in res if x]))
        return


def nme(event):
    if len(event.args) != 2:
        event.reply('name <stringinurl> <name>')
        return
    selector = {'rss': event.args[0]}
    for feed in find('rss', selector):
        if feed:
            feed.name = event.args[1]
            write(feed)
    event.reply('ok')


def rem(event):
    if len(event.args) != 1:
        event.reply('rem <stringinurl>')
        return
    selector = {'rss': event.args[0]}
    for feed in find('rss', selector):
        if feed:
            feed.__deleted__ = True
            write(feed)
    event.reply('ok')


def rss(event):
    if not event.rest:
        nrs = 0
        for feed in find('rss'):
            event.reply('%s %s %s' % (
                                   nrs,
                                   printable(feed),
                                   elapsed(time.time()-fntime(feed.__oid__))
                                  )
                       )
            nrs += 1
        if not nrs:
            event.reply('no rss feed found.')
        return
    url = event.args[0]
    if 'http' not in url:
        event.reply('i need an url')
        return
    for res in find('rss', {'rss': url}):
        if res:
            event.reply('already got %s' % url)
            return
    feed = Rss()
    feed.rss = event.args[0]
    write(feed)
    event.reply('ok')
