import re
from functools import reduce
from typing import Dict
import operator
import yaml
from pyparsing import Group, Opt, ParserElement, ZeroOrMore, Regex, oneOf
from jianzipu.constant import *


# fingers, modifiers and markers are open, so we import from outside
with open('./jianzipu/data.yaml', 'r', encoding='utf-8') as f:
  d: Dict[str, Dict[str, str]] = yaml.safe_load(f)
# 保证字符长的在前（如防止勾剔只匹配了勾）
HUI_FINGER = sorted(d['徽位指法'].keys(), key=len, reverse=True)
XIAN_FINGER = sorted(d['弦序指法'].keys(), key=len, reverse=True)
MOVE_FINGER = sorted(d['走位指法'].keys(), key=len, reverse=True)
SPECIAL_FINGER = sorted(d['特殊指法'].keys(), key=len, reverse=True)
MODIFIER = sorted(d['修饰'].keys(), key=len, reverse=True)
BOTH_FINGER = sorted(d['联袂指法'].keys(), key=len, reverse=True)
COMPLEX_FINGER = sorted(d['复式指法'].keys(), key=len, reverse=True)
MARKER = sorted(d['记号'].keys(), key=len, reverse=True)

# numbers are closed, so we list here
XIAN = ['一弦','二弦','三弦','四弦','五弦','六弦','七弦']
HUI = ['十一徽','十二徽','十三徽','一徽','二徽','三徽','四徽','五徽','六徽','七徽','八徽','九徽','十徽']
FEN = ['一分','二分','三分','四分','五分','六分','七分','八分','九分','半']

# 我们禁止谱字读法中间出现空格，空格用于分割
ParserElement.set_default_whitespace_chars('')
# Define individual components
hui = (ZeroOrMore((oneOf(HUI) + Opt(oneOf(FEN))) | '徽外')).set_results_name('hui')
xian = (ZeroOrMore(oneOf(XIAN))).set_results_name('xian')
hui_finger = oneOf(HUI_FINGER).set_results_name('hui_finger')
xian_finger = oneOf(XIAN_FINGER).set_results_name('xian_finger')
move_finger = oneOf(MOVE_FINGER).set_results_name('move_finger')
special_finger = oneOf(SPECIAL_FINGER).set_results_name('special_finger')
modifier = oneOf(MODIFIER).set_results_name('modifier')
both_finger = oneOf(BOTH_FINGER).set_results_name('both_finger')
complex_finger = oneOf(COMPLEX_FINGER).set_results_name('complex_finger')
marker = oneOf(MARKER).set_results_name('marker')

# Define phrase patterns
hui_finger_phrase = Group(hui_finger + hui).set_results_name('hui_finger_phrase')
xian_finger_phrase = Group(xian_finger + xian).set_results_name('xian_finger_phrase')
left_sub_phrase = Group(hui_finger_phrase + Opt(special_finger) + xian).set_results_name('left_sub_phrase')
right_sub_phrase = Group(hui_finger_phrase + Opt(special_finger) + xian).set_results_name('right_sub_phrase')

# Define form pattern
simple_form = Group(Opt(hui_finger_phrase) + Opt(special_finger) + Opt(xian_finger_phrase)).set_results_name('simple_form')
complex_form = Group(complex_finger + left_sub_phrase + right_sub_phrase).set_results_name('complex_form')
aside_form = Group(Opt(modifier) + move_finger + hui).set_results_name('aside_form')

# 谱字, lazy matching, order is important
PUZI = marker | both_finger | aside_form | complex_form | simple_form  

# IDC
class IDC:
  left_right='⿰'
  above_below='⿱'
  left_middle_right='⿲'
  above_middle_below='⿳'
  full_surround='⿴'
  surround_above='⿵'
  surround_below='⿶'
  surround_left='⿷'
  surround_upper_left='⿸'
  surround_upper_right='⿹'
  surround_lower_left='⿺'
  overlaid='⿻'

NUMBER_CHAR = {
 '一': '一',
 '二': '二',
 '三': '三',
 '四': '四',
 '五': '五',
 '六': '六',
 '七': '七',
 '八': '八',
 '九': '九',
 '十': '十',
 '十一': '⿸十一',
 '十二': '⿸十二',
 '十三': '⿸十三',
 '外': '卜',
 '半': '半'
}

JIANZI_CHAR = reduce(operator.ior, [*d.values(), NUMBER_CHAR], {})

# valence of fingers, for linting
VALENCE = {
          '散音':0,'大指':1,'食指':1,'中指':1,'名指':1,'跪指':1,
          #,'就',
          #'进','退','复进','复退','复','引上','淌下','往来','撞','掐起','带起',
          #'罨','推出','不动',

          '擘':1,'托':1,'抹':1,'挑':1,'勾':1,'剔':1,'打':1,'摘':1,'抹挑':1,'勾剔':1,
          '历':2,
          # '蠲','轮','琐','长琐',
          #'如一声','双弹','拨','剌','拨剌','伏','撮','打圆','滚','拂','滚拂','全扶'

          '分开':0,'同声':0,'应合':0,'放合':0,'掐撮声':0,'掐撮三声':0
          }