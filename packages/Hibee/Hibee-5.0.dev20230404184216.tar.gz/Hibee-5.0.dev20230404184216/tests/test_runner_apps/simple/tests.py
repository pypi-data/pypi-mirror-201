from unittest import TestCase

from hibee.test import SimpleTestCase
from hibee.test import TestCase as HibeeTestCase


class HibeeCase1(HibeeTestCase):
    def test_1(self):
        pass

    def test_2(self):
        pass


class HibeeCase2(HibeeTestCase):
    def test_1(self):
        pass

    def test_2(self):
        pass


class SimpleCase1(SimpleTestCase):
    def test_1(self):
        pass

    def test_2(self):
        pass


class SimpleCase2(SimpleTestCase):
    def test_1(self):
        pass

    def test_2(self):
        pass


class UnittestCase1(TestCase):
    def test_1(self):
        pass

    def test_2(self):
        pass


class UnittestCase2(TestCase):
    def test_1(self):
        pass

    def test_2(self):
        pass

    def test_3_test(self):
        pass
