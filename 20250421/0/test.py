import unittest
import prog


class Test(unittest.TestCase):
    def test_0(self):
        self.assertEqual(prog.sqroots("1 2 3"), '0')

    def test_1(self):
        self.assertEqual(prog.sqroots("1 2 1"), '1')

    def test_2(self):
        self.assertEqual(prog.sqroots("1 5 6"), '2')




