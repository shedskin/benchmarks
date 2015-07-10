# Write the benchmarking functions here.
# See "Writing benchmarks" in the asv docs for more information.

import os

import asv.util

cwd = os.getcwdu()
testdir = os.path.sep.join([cwd, "microtests"])


class Testing(object):
    def compile(self, name):
        """
        Compile @name.
        """
        os.chdir(testdir)
        asv.util.check_call("shedskin %s" % name, shell=True)
        asv.util.check_call("make")
        os.chdir(cwd)

    def run_test(self, test):
        binary = os.path.sep.join([testdir, test])
        cmd = "%s > /dev/null" % binary
        asv.util.check_call(cmd, shell=True)


class Startup(Testing):
    """
    Benchmark all startup tests.
    """
    def setup(self):
        self.compile("empty_startup.py")

    def time_empty_startup(self):
        self.run_test("empty_startup")


class Printing(Testing):
    """
    Benchmark all printing tests.
    """
    def setup(self):
        self.compile("print_ints.py")

    def time_ints(self):
        self.run_test("print_ints")


class Reference(Testing):
    """
    Benchmark reference C/C++ tests.
    """
    folder = "reference"

    def setup(self):
        os.chdir(os.path.sep.join([cwd, self.folder]))
        asv.util.check_call("gcc empty_startup.c -o empty_startup", shell=True)
        os.chdir(cwd)

    #def time_empty_startup(self):
    #    binary = os.path.sep.join([cwd, self.folder, "empty_startup"])
    #    cmd = "%s > /dev/null" % binary
    #    asv.util.check_call(cmd, shell=True)
