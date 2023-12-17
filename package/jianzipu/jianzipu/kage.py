# 定义组合图式的KAGE变换
from functools import reduce
import operator
import os
from typing import Dict, Literal, Self, ClassVar
from dataclasses import dataclass
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

# workaround for non published kage-python package
import sys
sys.path.append('/home/mao/workspace/kage-engine')

@dataclass
class Kage:
    CACHE: ClassVar[dict[str, str]] = CLOSURE
    key: str = ''
    data: str = ''

    def __post_init__(self):
        self.CACHE[self.key] = self.data

    @classmethod
    def primitive(cls, name):
        if name is None:
            return None
        if name in KAGE:
            return cls(name, CLOSURE[KAGE[name]])
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
        key = f'({top.key}&{bottom.key})'
        top_box = f'99:0:0:0:0:{DPI}:{DPI*ratio2}:{top.key}:0:0:0'
        bottom_box = f'99:0:0:0:{DPI*ratio1}:{DPI}:{DPI}:{bottom.key}:0:0:0'
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
                ratio1, ratio2 = 0.8, 0.4
        key = f'({left.key}&{right.key})'
        left_box = f'99:0:0:0:0:{DPI*ratio1}:{DPI}:{left.key}:0:0:0'
        right_box = f'99:0:0:{DPI*ratio2}:0:{DPI}:{DPI}:{right.key}:0:0:0'
        data = f'{left_box}${right_box}'
        return cls(key, data)
    
    @classmethod
    def top_left_right(cls, top: Self, bottom_left: Self, bottom_right: Self):
        key = f'({top.key}&{bottom_left.key}&{bottom_right.key})'
        top_box = f'99:0:0:0:0:{DPI}:{DPI*0.4}:{top.key}:0:0:0'
        bottom_left_box = f'99:0:0:0:66:168:200:{bottom_left.key}:0:0:0'
        bottom_right_box = f'99:0:0:60:66:200:200:{bottom_right.key}:0:0:0'
        data = f'{top_box}${bottom_left_box}${bottom_right_box}'
        return cls(key, data)



    @classmethod
    def finger_phrase(cls, finger_kage: Self, number_kage: Self):
        a = finger_kage is not None
        b = number_kage is not None
        match a,b:
            case True, False:
                return finger_kage
            case False, True:
                return number_kage
            case True, True:
                key = f'({finger_kage.key}&{number_kage.key})'
                match finger_kage.key:
                    case '勾':
                        data = f'99:0:0:0:0:200:200:{finger_kage.key}:0:0:0$99:0:0:44:50:158:167:{number_kage.key}:0:0:0'
                    case '剔':
                        data = f'99:0:0:0:0:200:200:{finger_kage.key}:0:0:0$99:0:0:36:88:162:176:{number_kage.key}:0:0:0'
                    case '抹':
                        data = f'99:0:0:0:0:200:248:{finger_kage.key}:0:0:0$99:0:0:0:105:200:200:{number_kage.key}:0:0:0'
                    case '挑':
                        data = f'99:0:0:0:0:200:200:{finger_kage.key}:0:0:0$99:0:0:30:21:180:167:{number_kage.key}:0:0:0'
                    case '托':
                        data = f'99:0:0:0:0:200:200:{finger_kage.key}:0:0:0$99:0:0:69:42:186:142:{number_kage.key}:0:0:0'
                    case '擘':
                        data = f'99:0:0:0:0:200:200:{finger_kage.key}:0:0:0$99:0:0:34:78:190:193:{number_kage.key}:0:0:0'
                    case '打':
                        data = f'99:0:0:0:0:200:200:{finger_kage.key}:0:0:0$99:0:0:16:52:150:150:{number_kage.key}:0:0:0'
                    case '摘':
                        data = f'99:0:0:0:0:200:200:{finger_kage.key}:0:0:0$99:0:0:20:80:166:177:{number_kage.key}:0:0:0'
                    case '勾剔':
                        data = f'99:0:0:0:0:200:200:{finger_kage.key}:0:0:0$99:0:0:35:108:162:176:{number_kage.key}:0:0:0'
                    case '抹挑':
                        data = f'99:0:0:0:0:200:200:{finger_kage.key}:0:0:0$99:0:0:45:100:174:168:{number_kage.key}:0:0:0'
                    case '托擘':
                        data = f'99:0:0:0:0:200:200:{finger_kage.key}:0:0:0$99:0:0:86:75:190:153:{number_kage.key}:0:0:0'
                    case '打摘':
                        data = f'99:0:0:0:0:200:200:{finger_kage.key}:0:0:0$99:0:0:23:99:165:176:{number_kage.key}:0:0:0'
                    case '历':
                        data = f'99:0:0:0:0:200:200:{finger_kage.key}:0:0:0$99:0:0:40:30:188:187:{number_kage.key}:0:0:0'
                    case '蠲':
                        data = f'99:0:0:0:0:200:200:{finger_kage.key}:0:0:0$99:0:0:45:100:174:168:{number_kage.key}:0:0:0'
                    case '轮':
                        data = f'99:0:0:0:0:200:100:{finger_kage.key}:0:0:0$99:0:0:0:100:200:200:{number_kage.key}:0:0:0'
                    case '半轮':
                        data = f'99:0:0:0:0:200:100:{finger_kage.key}:0:0:0$99:0:0:0:100:200:200:{number_kage.key}:0:0:0'
                    case '琐':
                        data = f'99:0:0:0:0:200:100:{finger_kage.key}:0:0:0$99:0:0:0:100:200:200:{number_kage.key}:0:0:0'
                    case '长琐':
                        data = f'99:0:0:0:0:200:100:{finger_kage.key}:0:0:0$99:0:0:0:100:200:200:{number_kage.key}:0:0:0'
                    case '滚'|'拂':
                        data = f'99:0:0:0:0:200:100:{finger_kage.key}:0:0:0$99:0:0:0:100:200:200:{number_kage.key}:0:0:0'
                    case '至':
                        data = f'99:0:0:0:-7:200:193:{finger_kage.key}:0:0:0$99:0:0:0:100:200:200:{number_kage.key}:0:0:0'
                    # hui finger
                    case '大指' | '食指' | '中指' | '名指' | '跪指' | '大' | '食' | '中' | '名' | '跪':
                        return Kage.left_right(finger_kage, number_kage, kind='hui')
                    case '散音' | '散':
                        return Kage.top_bottom(finger_kage, number_kage, kind='finger')
                    # moving finger
                    case '上'|'下':
                        data = f'99:0:0:40:0:160:100:{finger_kage.key}:0:0:0$99:0:0:40:100:160:200:{number_kage.key}:0:0:0'
                    case _:
                        raise NotImplementedError
                return cls(key, data)

    @classmethod
    def simple_form(cls, hui_finger_phrase_kage: Self, xian_finger_phrase_kage: Self, special_finger_kage: Self):
        a = hui_finger_phrase_kage is not None
        b = xian_finger_phrase_kage is not None
        c = special_finger_kage is not None
        match a,b,c:
            case True, True, True:
                return Kage.top_left_right(hui_finger_phrase_kage, special_finger_kage, xian_finger_phrase_kage)
            case True, True, False:
                return Kage.top_bottom(hui_finger_phrase_kage, xian_finger_phrase_kage, kind='finger')
            case False, True, True:
                return Kage.left_right(special_finger_kage, xian_finger_phrase_kage, kind='xian')
            case False, True, False:
                return xian_finger_phrase_kage
    
    @classmethod
    def complex_form(cls, complex_finger_kage: Self, left_sub_phrase_kage: Self, right_sub_phrase_kage: Self):
        match complex_finger_kage.key:
            case '撮':
                key = f'({complex_finger_kage.key}&{left_sub_phrase_kage.key}&{right_sub_phrase_kage.key})'
                data = f'99:0:0:0:0:200:200:{complex_finger_kage.key}:0:0:0$99:0:0:14:78:94:184:{left_sub_phrase_kage.key}:0:0:0$99:0:0:105:78:187:180:{right_sub_phrase_kage.key}:0:0:0'
            case _:
                return NotImplementedError
        return cls(key, data)
    
    @classmethod
    def aside_form(cls, modifier_kage: Self, special_finger_kage: Self, move_finger_phrase: Self):
        a = modifier_kage is not None
        b = special_finger_kage is not None
        c = move_finger_phrase is not None
        match a,b,c:
            case True, True, True:
                return Kage.top_left_right(modifier_kage, special_finger_kage, move_finger_phrase)
            case True, False, True:
                return Kage.top_bottom(modifier_kage, move_finger_phrase)
            case False, True, True:
                return Kage.left_right(special_finger_kage, move_finger_phrase)
            case False, False, True:
                return move_finger_phrase

    def draw(self):
        from kage import Kage as KageEngine
        kage_engine = KageEngine(ignore_component_version=True)
        for k, v in self.CACHE.items():
            kage_engine.components.push(k, v)
        canvas = kage_engine.make_glyph(self.key)
        return canvas
