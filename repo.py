#!/usr/bin/python2.6

import crawler
import time
import os
import pysvn
import string
import urllib2
import urlparse

svn_repos = 'file:///home/bhagya/Workspace/RadheshSir/work/repos/'

class Repo:
    base = ''
    base_len = 0
    dir_name = ''
    def __init__ (self, baseurl):
        url_comp = urlparse.urlparse (baseurl)
        if url_comp.scheme == '':
            baseurl = 'http://' + baseurl
        self.base = baseurl
        self.base_len = len (self.base)
        url_comp = urlparse.urlparse (self.base)
        self.dir_name = url_comp.netloc

    def init (self):

        c = crawler.Crawler (self.base)
        svn_cli = pysvn.Client ()

        if not os.path.isdir (self.dir_name):
            os.mkdir (self.dir_name)

        print 'CRAWLING...'
        url_lst = c.crawl ()
        print 'FETCHING...'
        for url in url_lst:
            try:
                res = urllib2.urlopen (url)
            except urllib2.URLError:
                continue
            print url
            fname = self.dir_name + '/'  + string.replace (url,'/','_')
            f = open (fname, 'w')
            f.write (res.read ())
            f.close ()

        svn_cli.import_ (self.dir_name, svn_repos + self.dir_name, 'Initial import')
        
        print 'Repo created at ' + svn_repos + self.dir_name
        print 'Working copy at ' + self.dir_name

    def update (self):
        c = crawler.Crawler (self.base)
        svn_cli = pysvn.Client ()

        if not os.path.isdir (self.dir_name):
            os.mkdir (self.dir_name)

        try:
            svn_cli.checkout (svn_repos + self.dir_name, self.dir_name)
        except pysvn._pysvn_2_6.ClientError:
            print "Repository doesn't exist! Use init() to create one."
            quit ()

        print 'CRAWLING...'
        url_lst = c.crawl ()
        print 'FETCHING...'
        for url in url_lst:
            try:
                res = urllib2.urlopen (url)
            except urllib2.URLError:
                continue
            print url
            fname = self.dir_name + '/'  + string.replace (url,'/','_')
            f = open (fname, 'w')
            f.write (res.read ())
            f.close ()

        timestamp = time.asctime (time.localtime(time.time()))

        svn_diff_text = svn_cli.diff('', self.dir_name)
        if svn_diff_text is not '':
            svn_cli.checkin (self.dir_name, timestamp)
        else:
            svn_diff_text = 'No change since last revision!'

        print 'Updated Repo!'
        print 'Updated files at ' + self.dir_name
        return svn_diff_text
