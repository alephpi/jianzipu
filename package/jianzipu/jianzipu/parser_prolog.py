import os
import janus_swi as janus 
from typing import Literal,List
import pprint as pp
import re

from .grammar import Note
from .constant import d

pwd = os.path.dirname(os.path.abspath(__file__))

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

NUMBER = ['十一','十二','十三','一','二','三','四','五','六','七','八','九','十','外','半']
HUI_FINGER = ['大','食','中','名','跪','散']
ALL = HUI_FINGER + XIAN_FINGER + MOVE_FINGER + SPECIAL_FINGER + BOTH_FINGER + COMPLEX_FINGER + MODIFIER + MARKER + NUMBER

def tokenizer(s:str) -> List[str]:
    sep = '指|徽|分|弦|音'
    simplified = re.sub(sep,' ', s)
    keep_pattern = '|'.join(ALL)
    tokens = re.split(f'({keep_pattern})', simplified)
    tokens = list(filter(lambda x: x.strip()!='', tokens))
    return tokens

def parser(tokens: list[str]):
    # with open('parser.pl', 'r', encoding='utf-8') as f:
    #     s = f.read()
    # janus.consult(data=s)
    janus.consult(file=pwd+'/parser.pl')
    result = janus.query_once(f'parser(Tree,{tokens},[])',keep=True)
    if result['truth']:
        return result['Tree']
    else:
        raise ValueError('Parse failed')