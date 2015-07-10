# Write the benchmarking functions here.
# See "Writing benchmarks" in the asv docs for more information.

import os
import subprocess

cwd = os.getcwdu()
testdir = os.path.sep.join([cwd, "microtests"])


class Testing(object):
    def compile(self, name):
        """
        Compile @name.
        """
        os.chdir(testdir)
        subprocess.call("shedskin %s" % name, shell=True)
        subprocess.call("make")
        os.chdir(cwd)


class Printing(Testing):
    """
    A benchmark that tests the various print_*.py functions in the microtests
    directory.
    """
    def setup(self):
        self.compile("print_ints.py")

    def time_ints(self):
        subprocess.call(os.path.sep.join([testdir, "print_ints"]))
