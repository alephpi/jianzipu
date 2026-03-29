import operator
import os
from functools import reduce
from pathlib import Path
from typing import Dict, Literal

import pandas as pd

TAG = (
    'SF','CF','AF','TF',
    'hfp', 'xfp', 'lsp', 'rsp', 'mfp',
    'hf', 'hn1', 'hn2', 'xf', 'xn1', 'xn2','sf','cf','jf','mo','ma'
    )

FORMS = ("SF", "CF", "AF", "TF")

# define syntax tag
t_TAG = Literal[
    'SF','CF','AF','TF',
    'hfp', 'xfp', 'lsp', 'rsp', 'mfp',
    'hf', 'hn1', 'hn2', 'xf', 'xn1', 'xn2','sf','cf','jf','mo','ma'
    ]


# TODO
t_JIANZI = str

# Get the current directory of the script
current_directory = Path(__file__).resolve().parent

# Construct the full path to the file
PATH_TO_GLYPHS = current_directory / "data/glyphs.csv"
PATH_TO_FIGMA = current_directory / "data/figma.css"

# with open(full_path, 'r', encoding='utf-8') as f:
GLYPHS = pd.read_csv(PATH_TO_GLYPHS, index_col=None)

HUI_FINGER = sorted(GLYPHS.query("GlyphTag == 'hf'").GlyphNameCN.tolist(), key=len, reverse=True)
XIAN_FINGER = sorted(GLYPHS.query("GlyphTag == 'xf'").GlyphNameCN.tolist(), key=len, reverse=True)
MOVE_FINGER = sorted(GLYPHS.query("GlyphTag == 'mf'").GlyphNameCN.tolist(), key=len, reverse=True)
SPECIAL_FINGER = sorted(GLYPHS.query("GlyphTag == 'sf'").GlyphNameCN.tolist(), key=len, reverse=True)
MODIFIER = sorted(GLYPHS.query("GlyphTag == 'mo'").GlyphNameCN.tolist(), key=len, reverse=True)
JOINT_FINGER = sorted(GLYPHS.query("GlyphTag == 'jf'").GlyphNameCN.tolist(), key=len, reverse=True)
COMPLEX_FINGER = sorted(GLYPHS.query("GlyphTag == 'cf'").GlyphNameCN.tolist(), key=len, reverse=True)
MARKER = sorted(GLYPHS.query("GlyphTag == 'ma'").GlyphNameCN.tolist(), key=len, reverse=True)
XIAN_NUMBER_ORTHO = ['一弦','二弦','三弦','四弦','五弦','六弦','七弦']
HUI_NUMBER_ORTHO = ['十一徽','十二徽','十三徽','一徽','二徽','三徽','四徽','五徽','六徽','七徽','八徽','九徽','十徽']
FEN_NUMBER_ORTHO = ['一分','二分','三分','四分','五分','六分','七分','八分','九分','半']
HUI_FINGER_ORTHO = ['大指','食指','中指','名指','跪指','散音']
XIAN_NUMBER_ABBR = ['一','二','三','四','五','六','七']
HUI_NUMBER_ABBR = ['十一','十二','十三','一','二','三','四','五','六','七','八','九','十']
FEN_NUMBER_ABBR = ['一','二','三','四','五','六','七','八','九','半']

JIANZI = GLYPHS.GlyphNameCN.tolist()
EN_from_CN: Dict[str, str] = dict(zip(GLYPHS.GlyphNameCN, GLYPHS.GlyphName))
CN_from_EN: Dict[str, str] = dict(zip(GLYPHS.GlyphName, GLYPHS.GlyphNameCN))

# valence of fingers, for linting
# VALENCE = {
#           '散音':0,'大指':1,'食指':1,'中指':1,'名指':1,'跪指':1,
#           #,'就',
#           #'进','退','复进','复退','复','引上','淌下','往来','撞','掐起','带起',
#           #'罨','推出','不动',

#           '擘':1,'托':1,'抹':1,'挑':1,'勾':1,'剔':1,'打':1,'摘':1,'抹挑':1,'勾剔':1,
#           '历':2,
#           # '蠲','轮','琐','长琐',
#           #'如一声','双弹','拨','剌','拨剌','伏','撮','打圆','滚','拂','滚拂','全扶'

#           '分开':0,'同声':0,'应合':0,'放合':0,'掐撮声':0,'掐撮三声':0
#           }