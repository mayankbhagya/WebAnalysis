#!/usr/bin/python2.6

import differ
import urllib2

f1 = open ('home.html','r')
f2 = open ('home2.html', 'r')

d = differ.Differ ()
difflst = d.diff (f1.read(), f2.read(), 1, 'sample.cfg')
for x in difflst:
    print x
    d.print_pretty_diff (difflst[x])
    print ''



