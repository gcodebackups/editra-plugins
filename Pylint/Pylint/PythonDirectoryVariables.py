# -*- coding: utf-8 -*-
# Name: PythonDirectoryVariables.py
# Purpose: Pylint plugin
# Author: Mike Rans
# Copyright: (c) 2010 Mike Rans
# License: wxWindows License
##############################################################################
""" Directory Variables module for Python data """

__version__ = "0.2"
__author__ = "Mike Rans"
__svnid__ = "$Id$"
__revision__ = "$Revision$"

#-----------------------------------------------------------------------------#

import os
from AbstractDirectoryVariables import AbstractDirectoryVariables

class PythonDirectoryVariables(AbstractDirectoryVariables):
    def __init__(self):
        AbstractDirectoryVariables.__init__(self, "py")
        self.addedpythonpaths = []

    @staticmethod
    def get_abspath(dirvarfile, path):
        if path != "":
            if path[0] == ".":
                dir, _ = os.path.split(dirvarfile)
                path = os.path.join(dir, path)
        return os.path.abspath(path)

    def recurseup(self, dir):
        dir, rest = os.path.split(dir)
        dirvarfile = os.path.join(dir, self.dirvarfilename)
        if os.path.isfile(dirvarfile):
            return dirvarfile
        if not rest:
            return None
        return self.recurseup(dir)

    def read_dirvarfile(self, filepath):
        dirvarfile = self.recurseup(filepath)
        if not dirvarfile:
            return {}
        dirvarfile = os.path.abspath(dirvarfile)
        file = open(dirvarfile)
        vardict = {}
        vardict["DIRVARFILE"] = dirvarfile
        for line in file:
            if not line or line.find("=") == -1:
                continue
            key, valstr = line.split("=")
            val = valstr.rstrip()
            if key == "PYTHONPATH":
                allnewpaths = val.split(",")
                for path in allnewpaths:
                    self.addedpythonpaths.append(self.get_abspath(dirvarfile, path))
            elif key == "PYLINTRC":
                vardict["PYLINTRC"] = '"%s"' % self.get_abspath(dirvarfile, val)
        vardict["ADDEDPYTHONPATHS"] = self.addedpythonpaths
        return vardict