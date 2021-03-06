"""
Flat binary workspace object

"""

import glob
from .memfbf import *


class Workspace(object):
    """
    A workspace provides a convenient way to access a directory of FBF files as workspace.['name'] or workspace.name syntax.
    """
    _vars = None
    path = None

    def __init__(self, dir='.'):
        """
        Initialize a workspace with a directory, capturing the initial list of variables in the workspace.
        :param dir: path to a directory to scan
        """
        self.path = dir
        self._vars = dict(self._scan_vars())

    def var(self, name):
        """
        return an FBF object for the given stem or filename.
        :param name: variable stem or filename
        :return: FBF object
        """
        v = self._vars.get(name, None)
        if v is not None:
            return v
        g = glob.glob(os.path.join(self.path, (name + '.*') if '.' not in name else name))
        if len(g) == 1:
            fbf = FBF(g[0])
            fbf.open()
            self._vars[fbf.stemname] = fbf
            return fbf
        raise AttributeError("{0:s} not in workspace".format(name))

    def _scan_vars(self):
        for path in os.listdir(self.path):
            try:
                x = FBF(os.path.join(self.path, path))
                yield x.stemname, x
            except ValueError:
                pass

    def variables(self):
        """
        Get the dictionary of variables found in the workspace at creation time
        :return: dict
        """
        return self._vars

    def __getitem__(self, name):
        return self.var(name)

    def __getattr__(self, name):
        return self.var(name)

    def absorb(self, stemname, nparray):
        """
            Absorb a numpy array into the workspace, resulting in a read-write FBF object.
            Raises an EnvironmentError if there is a collision.
        """
        raise NotImplementedError('Not Yet Implemented')


def main():
    from sys import argv

    if len(argv) == 2:
        q = Workspace(argv[1])
        from pprint import pprint

        pprint(dict((x, str(y).split('\n')) for (x, y) in q.variables().items()))
    else:
        print("Usage: workspace.py <workspace-dir>")


if __name__ == '__main__':
    main()
