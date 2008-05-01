#!/usr/bin/env python

from setuptools.command.test import test as _test

def _TestClass(base):
    class _test(base):
        description = base.description + ", for FiPy and its examples"

        # List of option tuples: long name, short name (None if no short
        # name), and help string.
        user_options = base.user_options + [
            ('inline', None, "run FiPy with inline compilation enabled"),
            ('Trilinos', None, "run FiPy using Trilinos solvers"),
            ('Pysparse', None, "run FiPy using Pysparse solvers (default)"),
            ('all', None, "run all non-interactive FiPy tests (default)"),
            ('really-all', None, "run *all* FiPy tests (including those requiring user input)"),
            ('examples', None, "test FiPy examples"),
            ('modules', None, "test FiPy code modules"),
            ('viewers', None, "test FiPy viewer modules (requires user input)"),
            ('cache', None, "run FiPy with Variable caching"),
            ('no-cache', None, "run FiPy without Variable caching"),
           ]


        def initialize_options(self):
            base.initialize_options(self)
            
            self.all = False
            self.really_all = False
            self.examples = False
            self.modules = False
            self.viewers = False
            
            self.inline = False
            self.cache = False
            self.no_cache = True
            self.Trilinos = False
            self.Pysparse = False

        def finalize_options(self):
            noSuiteOrModule = (self.test_suite is None 
                               and self.test_module is None)
                
            base.finalize_options(self)
            
            if noSuiteOrModule:
                self.test_args.remove(self.distribution.test_suite)
                
            if not (self.examples or self.modules or self.viewers):
                self.all = True
            if self.all or self.really_all:
                self.examples = True
                self.modules = True
            if self.really_all:
                self.viewers = True
            
                
            if self.viewers:
                print "*" * 60
                print "*" + "".center(58) + "*"
                print "*" + "ATTENTION".center(58) + "*"
                print "*" + "".center(58) + "*"
                print "*" + "Some of the following tests require user interaction".center(58) + "*"
                print "*" + "".center(58) + "*"
                print "*" * 60
                
                self.test_args.append("fipy.viewers.testinteractive._suite")

            if self.modules:
                self.test_args.append("fipy.test._suite")
            
            if self.examples:
                self.test_args.append("examples.test._suite")

            if self.test_args and noSuiteOrModule:
                self.test_suite = "dummy"

    return _test                    
            
test = _TestClass(_test)

try:
    # we only need "unittest" if bitten is installed 
    # (and we're running as a bitten.slave)
    from bitten.util.testrunner import unittest as _unittest
    unittest = _TestClass(_unittest)
except ImportError, e:
    unittest = test
