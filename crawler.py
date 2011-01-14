#!/usr/bin/python2.6

import urlparse
import urllib2
import HTMLParser


def get_abs_url (baseurl, url):
    url_comp = urlparse.urlparse (url)
    scheme = url_comp.scheme
    if scheme is '':
        absurl = urlparse.urljoin (baseurl, url)
    else:
        absurl = url
    return absurl


class MyParser (HTMLParser.HTMLParser):
    url_lst = []
    def __init__ (self):
        HTMLParser.HTMLParser.__init__ (self)

    def feed_data (self, data):
        self.reset ()
        self.url_lst = []
        try:
            self.feed (data)
        except HTMLParser.HTMLParseError as err:
            print err

    def get_url_list (self):
        return self.url_lst

    def handle_starttag (self, tag, attrs):
        dattrs = dict (attrs)
        if tag == 'a':
            self.url_lst.append (dattrs['href'])


class Crawler:
    index = []
    base = ''
    base_len = 0
    def __init__ (self, base_url):
        url_comp = urlparse.urlparse (base_url)
        if url_comp.scheme == '':
            self.base = 'http://' + base_url
        else:
            self.base = base_url
        self.base_len = len (self.base)
        self.index.append (self.base)

    def crawl (self):
        parser = MyParser ()
        for url in self.index:
            print 'PROCESSING ' + url + '...'
            try:
                res = urllib2.urlopen (url)
            except urllib2.URLError:
                print "Erroneous URL!"
                continue
            parser.feed_data (res.read ())
            for u in parser.get_url_list ():
                abs_u = get_abs_url (url, u)
                if (abs_u not in self.index) and abs_u[:self.base_len] == self.base:
                    self.index.append (abs_u)
                    print abs_u
        return self.index
