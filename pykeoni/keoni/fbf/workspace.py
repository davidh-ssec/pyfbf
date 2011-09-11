"""
$Id$
Flat Binary Format python utilities
parallel to TOOLS/Mfiles/fbf*.m
"""

import os,glob,exceptions

from keoni.fbf.numfbf import *  # originally in cvs/TOOLS/dev/maciek/python

class Workspace(object):
    def __init__(self,dir='.'):
        self._dir=dir

    def __getattr__(self,name):
        g = glob.glob( os.path.join(self._dir,name+'.*') )
        if len(g)==1:
            fp = FBF(g[0])
            fp.open()
            setattr(self,name,fp)
            return fp
        raise exceptions.AttributeError, "%s not in workspace" % name
        
    def var(self,name):
        return getattr(self, name)
    
    def vars(self):
        for path in os.listdir(self._dir):
            try:
                x = info(path)
                yield x.stemname, x
            except:
                pass
            
    def variables(self):
        return dict(self.vars())

    def __getitem__(self,name):
        return getattr(self,name)

    
if __name__=='__main__':
    from sys import argv
    fi = info(argv[1])
    data = read( fi )
    print data
    print fi
