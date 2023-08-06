import doctest
from unittest import TestCase

from hibee.test import SimpleTestCase
from hibee.test import TestCase as HibeeTestCase

from . import doctests


class TestVanillaUnittest(TestCase):
    def test_sample(self):
        self.assertEqual(1, 1)


class TestHibeeTestCase(HibeeTestCase):
    def test_sample(self):
        self.assertEqual(1, 1)


class TestZimpleTestCase(SimpleTestCase):
    # Z is used to trick this test case to appear after Vanilla in default suite

    def test_sample(self):
        self.assertEqual(1, 1)


class EmptyTestCase(TestCase):
    pass


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(doctests))
    return tests
