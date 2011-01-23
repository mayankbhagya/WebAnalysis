#!/usr/bin/python2.6

import time
import os
import pysvn

class Repo:
    svn_repo_url = ''
    def __init__ (self, svn_repo_path):
        svn_cli = pysvn.Client ()
        if not os.path.isdir (svn_repo_path):
            print "SVN repositories not found at the given location!"
            quit ()
        if svn_repo_path [-1:] != '/':
            svn_repo_path = svn_repo_path + '/'
        self.svn_repo_url = 'file://' + svn_repo_path

    def init (self, dir_name, repo_name):
        svn_cli = pysvn.Client ()

        if not os.path.isdir (dir_name):
            print "Directory doesn't exist! Can't init repository."
            quit ()

        try:
            svn_cli.import_ (dir_name, self.svn_repo_url + repo_name, 'Initial import')
        except:
            print 'SVN Error! Failed to import...'
            quit ()

        print 'Repo created at ' + self.svn_repo_url + dir_name
        print 'Working copy at ' + dir_name

    def update (self, dir_name, repo_name):
        svn_cli = pysvn.Client ()

        if not os.path.isdir (dir_name):
            print "Directory doesn't exist! Can't update repository."
            quit ()

        timestamp = time.asctime (time.localtime(time.time()))
        try:
            svn_cli.checkin (dir_name, timestamp)
        except:
            print "Can't update " + dir_name + '! SVN Error!'
            quit ()

        print 'Updated Repo!'

    def checkout (self, dir_name, repo_name):
        svn_cli = pysvn.Client ()
        if not os.path.isdir (dir_name):
            try:
                os.makedirs (dir_name)
            except:
                print 'Failed to create directory.'
                quit()

        svn_cli.checkout (self.svn_repo_url + repo_name, dir_name)

    def diff (self, dir_name):
        svn_cli = pysvn.Client ()
        try:
            svn_diff_text = svn_cli.diff('', dir_name)
        except:
            print 'SVN Error!'
            quit ()
        return svn_diff_text

