#!/usr/bin/python2.6

import crawler
import sys

#just in case your OS has proxy settings
#os.environ["http_proxy"] = "http://10.10.:80"

if len(sys.argv) == 1:
    print 'Enter URL!'
    quit ()
c = crawler.Crawler (sys.argv[1])
l = c.crawl ()
for x in l:
    print x
