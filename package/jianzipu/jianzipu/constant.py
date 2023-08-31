from functools import reduce
import operator
from typing import Dict
import yaml

with open('./jianzipu/ids.yaml', 'r', encoding='utf-8') as f:
  d: Dict[str, Dict[str, str]] = yaml.safe_load(f)



NUMBER = {
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
 '半': '𰀁' #扩G
}

JIANZI = reduce(operator.ior, [*d.values(), NUMBER], {})

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