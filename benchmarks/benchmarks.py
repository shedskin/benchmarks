# Write the benchmarking functions here.
# See "Writing benchmarks" in the asv docs for more information.

import os

import asv.util
import timeit

cwd = os.getcwdu()
testdir = os.path.sep.join([cwd, "microtests"])


class Testing(object):
    repeat = 100
    timeout = 600.0
    timer = timeit.default_timer

    def compile(self, name):
        """
        Compile @name. If @name is a list, loop over it.
        """
        os.chdir(testdir)
        if isinstance(name, list):
            for n in name:
                asv.util.check_call("shedskin %s" % n, shell=True)
                asv.util.check_call("make")
        else:
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
    tests = ["print_empty.py",
             "print_floats.py",
             "print_ints.py",
             "print_str.py",
            ]

    def setup(self):
        self.compile(self.tests)

    def time_empty(self):
        self.run_test("print_empty")

    def time_floats(self):
        self.run_test("print_ints")

    def time_ints(self):
        self.run_test("print_ints")

    def time_str(self):
        self.run_test("print_str")


class Reference(Testing):
    """
    Benchmark reference C/C++ tests.
    """
    folder = "reference"

    def setup(self):
        os.chdir(os.path.sep.join([cwd, self.folder]))
        asv.util.check_call("gcc empty_startup.c -o empty_startup", shell=True)
        os.chdir(cwd)

    # def time_empty_startup(self):
    #     binary = os.path.sep.join([cwd, self.folder, "empty_startup"])
    #     cmd = "%s > /dev/null" % binary
    #     asv.util.check_call(cmd, shell=True)
