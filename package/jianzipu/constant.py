import re
from functools import reduce
import operator
from typing import Dict
import yaml

# fingers, modifiers and markers are open, so we import from outside
with open('./jianzipu/data.yaml', 'r', encoding='utf-8') as f:
  d: Dict[str, Dict[str, str]] = yaml.safe_load(f)

# 保证字符长的在前（如防止勾剔只匹配了勾）
hui_finger = '|'.join(list(sorted(d['徽位指法'].keys(), key=len, reverse=True)))
xian_finger = '|'.join(list(sorted(d['弦序指法'].keys(), key=len, reverse=True)))
move_finger = '|'.join(list(sorted(d['走位指法'].keys(), key=len, reverse=True)))
special_finger = '|'.join(list(sorted(d['特殊指法'].keys(), key=len, reverse=True)))
modifier = '|'.join(list(sorted(d['修饰'].keys(), key=len, reverse=True)))
both_finger = '|'.join(list(sorted(d['联袂指法'].keys(), key=len, reverse=True)))
complex_finger = '|'.join(list(sorted(d['复式指法'].keys(), key=len, reverse=True)))
marker = '|'.join(list(sorted(d['记号'].keys(), key=len, reverse=True)))

# numbers are closed, so we list here
# XIAN_DOMAIN = ['一弦','二弦','三弦','四弦','五弦','六弦','七弦']
# HUI_DOMAIN = ['一徽','二徽','三徽','四徽','五徽','六徽','七徽','八徽','九徽','十徽','十一徽','十二徽','十三徽','徽外']
# FEN_DOMAIN = ['一分','二分','三分','四分','五分','六分','七分','八分','九分','半']

# BN-form see readme.md

## symbol pattern
XIAN = r'(?P<xian>(一弦|二弦|三弦|四弦|五弦|六弦|七弦)*)'
HUI = r'(?P<hui>((十一徽|十二徽|十三徽|一徽|二徽|三徽|四徽|五徽|六徽|七徽|八徽|九徽|十徽)(一分|二分|三分|四分|五分|六分|七分|八分|九分|半)?|徽外)*)'
HUI_FINGER = fr'(?P<hui_finger>{hui_finger})'
XIAN_FINGER = fr'(?P<xian_finger>{xian_finger})'
MOVE_FINGER = fr'(?P<move_finger>{move_finger})'
SPECIAL_FINGER = fr'(?P<special_FINGER>{special_finger})'
MODIFIER = fr'(?P<modifier>{modifier})'
BOTH_FINGER = fr'(?P<both_finger>{both_finger})'
COMPLEX_FINGER = fr'(?P<complex_finger>{complex_finger})'
MARKER = fr'(?P<marker>{marker})'

## phrase pattern
HUI_FINGER_PHRASE = fr'(?P<hui_finger_phrase>{HUI_FINGER}{HUI})'
XIAN_FINGER_PHRASE = fr'(?P<xian_finger_phrase>{XIAN_FINGER}{XIAN})'

## form pattern
SIMPLE_FORM = fr'(?P<common_form>{HUI_FINGER_PHRASE}?{SPECIAL_FINGER}?{XIAN_FINGER_PHRASE}?)'
COMPLEX_FORM = fr'(?P<complex_form>{COMPLEX_FINGER}{HUI_FINGER_PHRASE}{SPECIAL_FINGER}?{XIAN}{HUI_FINGER_PHRASE}{SPECIAL_FINGER}?{XIAN})'
ASIDE_FORM = fr'(?P<aside_form>{MODIFIER}*{MOVE_FINGER}+{HUI}*)'


# 谱字
PUZI = re.compile(fr'{SIMPLE_FORM}|{COMPLEX_FORM}|{ASIDE_FORM}|{MARKER}')

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