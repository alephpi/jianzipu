from itertools import product
import unittest


from .parser import parse
from .symbol import Leftor, Rightor, Bothor, Marker, Figure 

class TestParse(unittest.TestCase):
    def test_right_only(self):
      for right, xian in product(Rightor.domain, Figure.xian):
          s1 = right + xian + '弦'
          s2 = '散'+ s1

          self.assertEqual(parse(s1))