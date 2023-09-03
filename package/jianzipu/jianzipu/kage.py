# 定义组合图式的KAGE变换
from functools import reduce
import operator
import os
from typing import Dict, Literal, Self
from attr import dataclass
import yaml

# Get the current directory of the script
current_directory = os.path.dirname(os.path.abspath(__file__))

# Construct the full path to the file
relative_file_path = "kage.yaml"
full_path = os.path.join(current_directory, relative_file_path)

with open(full_path, 'r', encoding='utf-8') as f:
  KAGE: Dict[str, Dict[str, str]] = yaml.safe_load(f)

KAGE: Dict[str, str] = reduce(operator.ior, [*KAGE.values()], {})

# Construct the full path to the file
relative_file_path = "closure.yaml"
full_path = os.path.join(current_directory, relative_file_path)

with open(full_path, 'r', encoding='utf-8') as f:
  CLOSURE: Dict[str, str] = yaml.safe_load(f)

DPI = 200

@dataclass
class Kage:
    key: str
    data: str

    @classmethod
    def primitive(cls, name):
        if name is None:
            return cls('', '')
        if name in KAGE:
            return cls(KAGE[name], CLOSURE[KAGE[name]])
        else:
            raise KeyError(f'{name} is not in KAGE dictionary, check if you provide a primitive name')

    @classmethod
    def top_bottom(cls, top: Self, bottom: Self, kind: Literal['finger', 'number']):
        # ratio1: upper bound ratio of bottom box
        # ratio2: lower bound ratio of top box
        match kind:
            case 'finger':
                ratio1, ratio2 = 0.33, 0.4
            case 'number':
                ratio1, ratio2 = 0.5, 0.5
        key = '(' + top.key +'_'+ bottom.key + ')'
        top_box = f'99:0:0:0:{DPI*ratio2}:{DPI}:{DPI}:{top.key}:0:0:0'
        bottom_box = f'99:0:0:0:0:{DPI}:{DPI*ratio1}:{bottom.key}:0:0:0'
        data = f'{top_box}${bottom_box}'
        return cls(key, data)

    @classmethod
    def left_right(cls, left: Self, right: Self, kind: Literal['hui','xian']):
        # ratio1: right bound ratio of left box
        # ratio2: left bound ratio of right box
        match kind:
            case 'xian':
                ratio1, ratio2 = 0.33, 0.4
            case 'hui':
                ratio1, ratio2 = 1, 0.3
        key = '(' + left.key +'_'+ right.key + ')'
        left_box = f'99:0:0:0:0:{DPI*ratio1}:{DPI}:{left.key}:0:0:0'
        right_box = f'99:0:0:{DPI*ratio2}:0:{DPI}:{DPI}:{right.key}:0:0:0'
        data = f'{left_box}${right_box}'
        return cls(key, data)
    
    @classmethod
    def finger_phrase(cls, finger: Self, *number: Self):
        key = '(' + finger.key +'_'+ {'_'.join(n.key for n in number)} + ')'
        data = f'99:0:0:0:0:0:0:{DPI}:{finger.key}:0:0:0$99:0:0:0:0:0:{DPI}:{phrase.key}:0:0:0'
        return cls(key, data)