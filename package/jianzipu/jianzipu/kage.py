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

@dataclass
class Kage:
    CACHE: ClassVar[dict[str, str]] = CLOSURE
    key: str
    data: str

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
    def finger_phrase(cls, finger: Self, number: Self):
        key = f'({finger.key}&{number.key})'
        match finger.key:
            case '勾':
                data = f'99:0:0:0:0:200:200:{finger.key}:0:0:0$99:0:0:44:50:158:167:{number.key}:0:0:0'
            case '剔':
                data = f'99:0:0:0:0:200:200:{finger.key}:0:0:0$99:0:0:36:88:162:176:{number.key}:0:0:0'
            case '抹':
                data = f'99:0:0:0:0:200:248:{finger.key}:0:0:0$99:0:0:0:105:200:200:{number.key}:0:0:0'
            case '挑':
                data = f'99:0:0:0:0:200:200:{finger.key}:0:0:0$99:0:0:37:21:181:172:{number.key}:0:0:0'
            case '托':
                data = f'99:0:0:0:0:200:200:{finger.key}:0:0:0$99:0:0:69:42:186:142:{number.key}:0:0:0'
            case '擘':
                data = f'99:0:0:0:0:200:200:{finger.key}:0:0:0$99:0:0:34:78:190:193:{number.key}:0:0:0'
            case '打':
                data = f'99:0:0:0:0:200:200:{finger.key}:0:0:0$99:0:0:16:52:150:150:{number.key}:0:0:0'
            case '摘':
                data = f'99:0:0:0:0:200:200:{finger.key}:0:0:0$99:0:0:20:80:166:177:{number.key}:0:0:0'
            case '勾剔':
                data = f'99:0:0:0:0:200:200:{finger.key}:0:0:0$99:0:0:35:108:162:176:{number.key}:0:0:0'
            case '抹挑':
                data = f'99:0:0:0:0:200:200:{finger.key}:0:0:0$99:0:0:45:100:174:168:{number.key}:0:0:0'
            case _:
                # raise NotImplementedError
                return Kage.left_right(finger, number, kind='hui')
        return cls(key, data)

    @classmethod
    def simple_form(cls, hui_finger_phrase: Self, xian_finger_phrase: Self, special_finger: Self):
        a = hui_finger_phrase is not None
        b = xian_finger_phrase is not None
        c = special_finger is not None
        match a,b,c:
            case True, True, True:
                key = f'({hui_finger_phrase.key}&{special_finger.key}&{xian_finger_phrase.key})'
                top_box = f'99:0:0:0:0:{DPI}:{DPI*0.4}:{hui_finger_phrase.key}:0:0:0'
                bottom_left_box = f'99:0:0:0:66:168:200:{special_finger.key}:0:0:0'
                bottom_right_box = f'99:0:0:60:66:200:200:{xian_finger_phrase.key}:0:0:0'
                data = f'{top_box}${bottom_left_box}${bottom_right_box}'
                return cls(key, data)
            case True, True, False:
                return Kage.top_bottom(hui_finger_phrase, xian_finger_phrase, kind='finger')
            case False, True, True:
                return Kage.left_right(special_finger, xian_finger_phrase, kind='xian')
            case False, True, False:
                return xian_finger_phrase
    
    def draw(self, font:Literal['serif','sans']='serif'):
        from kage import Kage as KageEngine
        kage_engine = KageEngine(ignore_component_version=True)
        if font == 'sans':
            from kage.font import Sans
            kage_engine.font = Sans()
            for k, v in self.CACHE.items():
                kage_engine.components.push(k, v)
            canvas = kage_engine.make_glyph(self.key)
            return canvas
        elif font == 'serif':
        # only for test purpose
            import webbrowser
            url = "http://localhost:5501/package/jianzipu/test.html?kage={}"
            for k, v in self.CACHE.items():
                kage_engine.components.push(k, v)
            data = kage_engine.components.search(self.key)
            stroke_list = kage_engine.get_each_strokes(data)
            query_kage = '$'.join(str(stroke) for stroke in stroke_list)
            webbrowser.open(url.format(query_kage))