#!/usr/bin/python2.6

import lxml.html
import lxml.html.diff
import ConfigParser

def print_col (string, col):
    if col == 'red':
        print '\033[1;41m'+string+'\033[1;m'
    elif col == 'green':
        print '\033[1;42m'+string+'\033[1;m'
    elif col == gray:
        print '\033[1;47m'+string+'\033[1;m'
    else:
        print string

class Differ:
    def __init__ (self):
        pass

    def diff (self, old, new, mode = 0, cfg_file = ''):
        old = lxml.html.fromstring (old)
        new = lxml.html.fromstring (new)
        difftxt = {}
        if mode == 0:
            difftxt['*'] = lxml.html.diff.htmldiff (old, new)
            return difftxt
        else:
            cfg = ConfigParser.RawConfigParser ()
            cfg.read (cfg_file)
            for sec in cfg.sections ():
                xpath = './/' + sec
                xpath_attr = ''
                for opt in cfg.options (sec):
                    xpath_attr = xpath_attr + '@' + opt + '=\''  +  cfg.get (sec,opt) + '\' and '
                if xpath_attr is not '':
                    xpath_attr = xpath_attr [:-5]
                    xpath = xpath + '[' + xpath_attr + ']'
                #print xpath
                try:
                    oldel = old.findall (xpath)
                    newel = new.findall (xpath)
                except:
                    print 'Bad config file!'
                    difftxt['*'] = lxml.html.diff.htmldiff (old,new)
                    return difftxt
                
                if len(oldel) == 1 and len(newel) == 1:
                    oel_data = lxml.html.tostring(oldel[0])
                    nel_data = lxml.html.tostring(newel[0])
                    difftxt[sec] = lxml.html.diff.htmldiff (oel_data, nel_data)
                else:
                    print 'Xpath ambiguous or not found for section:' + sec + '!'

        return difftxt

    def print_pretty_diff (self, text):
        obj = lxml.html.fromstring (text)
        added = obj.findall ('.//ins')
        for x in added:
            txt = lxml.html.tostring (x)
            print_col (txt, 'green')
        deleted = obj.findall ('.//del')
        for x in deleted:
            txt = lxml.html.tostring (x)
            print_col (txt, 'red')
        
