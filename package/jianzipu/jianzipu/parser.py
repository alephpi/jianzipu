from typing import Literal
from pyparsing import Group, Opt, ParserElement, ZeroOrMore, oneOf

from .grammar import Note
from .constant import d 

# fingers, modifiers and markers are open, so we import from outside
# 保证字符长的在前（如防止勾剔只匹配了勾）
HUI_FINGER = sorted(d['徽位指法'].keys(), key=len, reverse=True)
XIAN_FINGER = sorted(d['弦序指法'].keys(), key=len, reverse=True)
MOVE_FINGER = sorted(d['走位指法'].keys(), key=len, reverse=True)
SPECIAL_FINGER = sorted(d['特殊指法'].keys(), key=len, reverse=True)
MODIFIER = sorted(d['修饰'].keys(), key=len, reverse=True)
BOTH_FINGER = sorted(d['联袂指法'].keys(), key=len, reverse=True)
COMPLEX_FINGER = sorted(d['复式指法'].keys(), key=len, reverse=True)
MARKER = sorted(d['记号'].keys(), key=len, reverse=True)


# white space is forbidden inside a note (but as a seperator between them)
ParserElement.set_default_whitespace_chars('')

class OrthoParseVar:
  # numbers are closed, so we list here
  XIAN = ['一弦','二弦','三弦','四弦','五弦','六弦','七弦']
  HUI = ['十一徽','十二徽','十三徽','一徽','二徽','三徽','四徽','五徽','六徽','七徽','八徽','九徽','十徽']
  FEN = ['一分','二分','三分','四分','五分','六分','七分','八分','九分','半']
  # Define individual components
  hui = (ZeroOrMore((oneOf(HUI) + Opt(oneOf(FEN))) | '徽外')).set_results_name('number')
  xian = (ZeroOrMore(oneOf(XIAN))).set_results_name('number')
  hui_finger = oneOf(HUI_FINGER).set_results_name('finger')
  xian_finger = oneOf(XIAN_FINGER).set_results_name('finger')
  move_finger = oneOf(MOVE_FINGER).set_results_name('finger')
  special_finger = oneOf(SPECIAL_FINGER).set_results_name('special_finger')
  modifier = oneOf(MODIFIER).set_results_name('modifier')
  both_finger = oneOf(BOTH_FINGER).set_results_name('both_finger')
  complex_finger = oneOf(COMPLEX_FINGER).set_results_name('complex_finger')
  marker = oneOf(MARKER).set_results_name('marker')

  # Define phrase patterns
  hui_finger_phrase = Group(hui_finger + hui).set_results_name('hui_finger_phrase')
  xian_finger_phrase = Group(xian_finger + xian).set_results_name('xian_finger_phrase')

  # reduced_xian_finger phrase, which is a simplified version of xian_finger_phrase
  # only used in complex from
  # since the complex_finger is actually the xian_finger 
  reduced_xian_finger_phrase = Group(xian).set_results_name('xian_finger_phrase')
  left_sub_phrase = Group(hui_finger_phrase + Opt(special_finger) + reduced_xian_finger_phrase).set_results_name('left_sub_phrase')
  right_sub_phrase = Group(hui_finger_phrase + Opt(special_finger) + reduced_xian_finger_phrase).set_results_name('right_sub_phrase')

  # move_finger_phrase is a similar to hui_finger_phrase, used in aside form
  move_finger_phrase = Group(move_finger + hui).set_results_name('move_finger_phrase')


  # Define form pattern
  # simple form must have xian_finger_phrase, while hui_finger_phrase is optional
  simple_form = Group(Opt(hui_finger_phrase) + Opt(special_finger) + xian_finger_phrase).set_results_name('simple_form')
  # complex form must have all
  complex_form = Group(complex_finger + left_sub_phrase + right_sub_phrase).set_results_name('complex_form')
  # similar for aside_form
  aside_form = Group(Opt(modifier) + Opt(special_finger) + move_finger_phrase).set_results_name('aside_form')

  # 谱字, lazy matching, order is important
  PUZI = complex_form | marker | both_finger | aside_form | simple_form

class AbbrParseVar:
  # numbers are closed, so we list here
  XIAN = ['一','二','三','四','五','六','七']
  HUI = ['十一','十二','十三','一','二','三','四','五','六','七','八','九','十']
  FEN = ['一','二','三','四','五','六','七','八','九','半']
  HUI_FINGER = ['大','食','中','名','跪','散']
  # Define individual components
  hui = (ZeroOrMore((oneOf(HUI) + Opt(oneOf(FEN))) | '外')).set_results_name('number')
  xian = (ZeroOrMore(oneOf(XIAN))).set_results_name('number')
  hui_finger = oneOf(HUI_FINGER).set_results_name('finger')
  xian_finger = oneOf(XIAN_FINGER).set_results_name('finger')
  move_finger = oneOf(MOVE_FINGER).set_results_name('finger')
  special_finger = oneOf(SPECIAL_FINGER).set_results_name('special_finger')
  modifier = oneOf(MODIFIER).set_results_name('modifier')
  both_finger = oneOf(BOTH_FINGER).set_results_name('both_finger')
  complex_finger = oneOf(COMPLEX_FINGER).set_results_name('complex_finger')
  marker = oneOf(MARKER).set_results_name('marker')

  # Define phrase patterns
  hui_finger_phrase = Group(hui_finger + hui).set_results_name('hui_finger_phrase')
  xian_finger_phrase = Group(xian_finger + xian).set_results_name('xian_finger_phrase')

  # reduced_xian_finger phrase, which is a simplified version of xian_finger_phrase
  # only used in complex from
  # since the complex_finger is actually the xian_finger 
  reduced_xian_finger_phrase = Group(xian).set_results_name('xian_finger_phrase')
  left_sub_phrase = Group(hui_finger_phrase + Opt(special_finger) + reduced_xian_finger_phrase).set_results_name('left_sub_phrase')
  right_sub_phrase = Group(hui_finger_phrase + Opt(special_finger) + reduced_xian_finger_phrase).set_results_name('right_sub_phrase')

  # move_finger_phrase is a similar to hui_finger_phrase, used in aside form
  move_finger_phrase = Group(move_finger + hui).set_results_name('move_finger_phrase')


  # Define form pattern
  # simple form must have xian_finger_phrase, while hui_finger_phrase is optional
  simple_form = Group(Opt(hui_finger_phrase) + Opt(special_finger) + xian_finger_phrase).set_results_name('simple_form')
  # complex form must have all
  complex_form = Group(complex_finger + left_sub_phrase + right_sub_phrase).set_results_name('complex_form')
  # similar for aside_form
  aside_form = Group(Opt(modifier) + Opt(special_finger) + move_finger_phrase).set_results_name('aside_form')

  # 谱字, lazy matching, order is important
  PUZI = complex_form | marker | both_finger | aside_form | simple_form


def parse(s: str, form = Literal['abbr','ortho']) -> Note:
  match form:
    case 'abbr':
      d = AbbrParseVar.PUZI.parse_string(s).as_dict()
    case 'ortho':
      d = OrthoParseVar.PUZI.parse_string(s).as_dict()
    case _:
      raise ValueError(f"form must be either 'abbr'or 'ortho'")
  print(d)
  # # linting
  # match xian_finger:
  #   case '历':
  #     assert len(xian) in [2,3], f'指法历的价位与弦序个数{len(xian)}不匹配'
  #   case _:
  #     assert VALENCE.get(xian_finger, 0) == len(xian), f'指法{xian_finger}的价位与弦序个数{len(xian)}不匹配'

  return Note.from_dict(d)

# def parse_xian(s: str, p=re.compile(r'(一弦|二弦|三弦|四弦|五弦|六弦|七弦)')) -> list[str]:
#   if s:
#     return p.findall(s)

# def parse_hui(s: str) -> list[str]:
#   if not s:
#     return
#   if s == '徽外':
#     return [s]
#   else:
#     index = s.index('徽')
#     return [s[:index+1], s[index+1:]]

# def parse_modifier(s: str, p=re.compile(r'(注|绰|吟|猱|上|下|急|缓|紧|慢)')) -> list[str]:
#   if s:
#     return p.findall(s)

def transcribe(s: str) -> str:
  """简写法转译为标准法
  """
  # 简单替换
  d = {
    '大': '大指',
    '食': '食指',
    '中': '中指',
    '名': '名指',
    '跪': '跪指',
    '散': '散音',
    '外': '徽外',
  }

  # 撮式
  if s[0] in COMPLEX_FINGER:

    left = s[:i+2]
    right = s[i+2:]
  # 旁注形式
  # 简单形式
  # 添加徽分弦
  for finger in XIAN_FINGER:
    i = s.find(finger)
    if i != -1:
      hui, xian = s[:i], s[i:]
      xian_finger, xian_number = xian[0:len(finger)], xian[len(finger):]
      if hui != '':
        if hui[-1] in ['绰','注']:
          special_finger = hui[-1]
          hui = hui[:-1]
        else:
          special_finger = ''
        hui_finger, hui_number = hui[0], hui[1:]
        hui_finger = d[hui_finger]
        if len(hui_number) == 1:
          if hui_number == '外':
            hui_number = '徽' + hui_number
          else:
            hui_number = hui_number + '徽'
        elif len(hui_number) == 2:
          if hui_number[0:2] in ['十一', '十二', '十三']:
            hui_number += '徽'
          else:
            hui_number = hui_number[0] + '徽' + hui_number[1] + '分'
        elif len(hui_number) == 3:
          hui_number = hui_number[0:2] + '徽' + hui_number[2] + '分'
        else:
          pass
      else:
        hui_finger = ''
        hui_number = ''
        special_finger = ''
      xian_number = ''.join(n+'弦' for n in xian_number)
      t = hui_finger + hui_number + special_finger + xian_finger + xian_number
      break
  
  return t