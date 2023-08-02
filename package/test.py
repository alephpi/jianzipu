import unittest

from jianzipu.parser import parse, parse_number

class TestParse(unittest.TestCase):
    def test_number(self):
       self.assertEqual(parse_number('十三徽半'), 13.5)
       self.assertEqual(parse_number('十徽九分'), 10.9)
       self.assertEqual(parse_number('七徽六分'), 7.6)
       self.assertEqual(parse_number('八徽四分'), 8.4)
       self.assertEqual(parse_number('徽外'), 14)

       self.assertEqual(parse_number('一弦'), 1)
       self.assertEqual(parse_number('五弦'), 5)
    
    def test_parse(self):
        l = ['大指七徽六分勾三弦',
             '跪指五徽八分挑六弦',
             '名指一徽九分注挑二弦',
             '食指十二徽半绰抹挑四弦',
             '中指徽外勾剔七弦',
             '中指徽外历二弦三弦',
            ]
        for i in l:
          self.assertEqual(str(parse(i)), i)

if __name__ == "__main__":
  suite = unittest.TestLoader().loadTestsFromTestCase(TestParse)
  runner = unittest.TextTestRunner()
  result = runner.run(suite)