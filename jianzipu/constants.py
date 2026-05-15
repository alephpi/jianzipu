from pathlib import Path
from typing import Dict, Literal

import pandas as pd

TAG = (
    'SF','CF','AF','TF',
    'hfp', 'xfp', 'lsp', 'rsp', 'mfp',
    'hf', 'hn1', 'hn2', 'xf', 'xn1', 'xn2', 'n',
    'sf','cf','jf','mo','ma'
    )

FORMS = ("SF", "CF", "AF", "TF")

# define syntax tag
t_TAG = Literal[
    'SF','CF','AF','TF',
    'hfp', 'xfp', 'lsp', 'rsp', 'mfp',
    'hf', 'hn1', 'hn2', 'xf', 'xn1', 'xn2', 'n',
    'sf','cf','jf','mf','mo','ma'
    ]

t_FORM = Literal['SF', 'CF', 'AF', 'TF']

# rearragne children tags in layout node for flattening trees in syntax order
CHILDREN_TAGS_ORDER_INDEX = {
    "SF": {"hfp": 0, "sf": 1, "xfp": 2},
    "CF": {"cf": 0, "lsp": 1, "rsp": 2},
    "hfp": {"hf": 0, "hn1": 1, "hn2": 2},
    "xfp": {"xf": 0, "xn1": 1, "xn2": 2},
}

# key: full layout, value: reduced layouts that inherit the full layout
REDUCED_FROM_FULL: dict[tuple[t_TAG, ...], list] = {
    ("hfp", "xfp"): [("hfp"), ("xfp")],
    ("hfp", "sf", "xfp"): [("hfp", "sf"), ("sf", "xfp"), ("sf")],
    ("xf", "xn1"): [("xf")],
    ("hf", "hn1"): [("hf")],
}

# TODO
t_JIANZI = str

# PATHS
# Get the working directory
PWD = Path(__file__).resolve().parent.parent

PATH_TO_GLYPHS = PWD / "data/glyphs.csv"
PATH_TO_FIGMA = PWD / "data/figma.css"
PATH_TO_FEATURES = PWD / "data/features.yaml"
PATH_TO_FEA = PWD / "data/output.fea"
PATH_TO_SVGS = PWD / "data/svgs"
PATH_TO_FONT = PWD / "font"

# with open(full_path, 'r', encoding='utf-8') as f:
GLYPHS = pd.read_csv(PATH_TO_GLYPHS, index_col=None).fillna('')
JIANZI = GLYPHS.GlyphNameCN.tolist()
EN_from_CN: Dict[str, str] = dict(zip(GLYPHS.GlyphNameCN, GLYPHS.GlyphName))
CN_from_EN: Dict[str, str] = dict(zip(GLYPHS.GlyphName, GLYPHS.GlyphNameCN))

# here only contains jianzi glyphs, not hanzi glyphs
JIANZI_ORDER = {}
for i, (glyph, vars) in enumerate(zip(GLYPHS.GlyphName, GLYPHS.Variant)):
    if vars:
        vars = vars.split(' ')
        for var in vars:
            JIANZI_ORDER[f"{glyph}.{var}"] = i

HANZI = [glyph for glyph in GLYPHS.GlyphNameCN.tolist() if len(glyph) == 1]

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