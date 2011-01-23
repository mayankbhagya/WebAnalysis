#!/usr/bin/python2.6

import repo
import sys

if len (sys.argv) == 1:
    print "Enter repository path setup by svnadmin!"
    quit ()

r = repo.Repo (sys.argv[1])
#To be run only once for a repository
#r.init ('/home/bhagya/Workspace/RadheshSir/work/test_repo', 'test_repo')

#To checkout a repository, i.e. to create a working copy
#r.checkout ('./test', 'test_repo')

#To update a repository
#r.update ('./test', 'test_repo')

#To compare two repositories
#t = r.diff ('./test')
#print t
