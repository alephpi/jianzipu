from abc import ABC, abstractmethod
from dataclasses import dataclass, field
import re

from .constant import JIANZI

class Element(ABC):
    """减字谱语法基本元素抽象类"""
    
    @abstractmethod
    def __str__(self) -> str:
        """返回对应的读法
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def ids(self) -> str:
        """返回对应的表意文字序列
        """
        raise NotImplementedError

@dataclass
class Symbol(Element):
    """减字符号的类

    Attributes:
        id (str): 减字符号的名称
        char (str): 减字符号的字面形式（文字或表意文字序列）
    """
    id: str = ''
    def __post_init__(self) -> None:
        self.char = JIANZI.get(self.id, '')

    def __str__(self) -> str:
        if self.id is None:
            return ''
        return self.id

    @property
    def ids(self) -> str:
        # remove format chars in token for single jianzi
        pattern = r'\[.*?\]'
        return re.sub(pattern, '', self.char).replace('〇','')

@dataclass
class Finger(Symbol):
    """指字符号的类
    """
    pass
@dataclass
class Number(Symbol):
    """数字符号的类
    """
    def __post_init__(self) -> None:
        key = self.id.replace('弦','').replace('徽','').replace('分','')
        self.char = JIANZI[key]

@dataclass
class Modifier(Symbol):
    """修饰符号的类
    """
    pass

@dataclass
class Marker(Symbol):
    """标记符号的类
    """
    pass

# @dataclass
# class Phrase:
#     cls = None
#     def __init__(self, tokens: list[str]) -> None:
#         self.tokens =  list(map(self.cls, tokens))

#     def __str__(self) -> str:
#         if not self.tokens:
#             return ''
#         return ''.join(str(token) for token in self.tokens)

# class NumberPhrase(Phrase):
#     cls = Number

# class ModifierPhrase(Phrase):
#     cls = Modifier

@dataclass
class FingerPhrase(Element):
    """指法短语的类

    Attributes:
        finger (Finger): 指法符号
        number (list[Number]): 数字符号列表

    """
    finger: Finger = None 
    number: list[Number] = field(default_factory=list)

    @classmethod
    def from_dict(cls, d) -> None:
        if isinstance(d, dict):
            finger = Finger(d.get('finger',''))
            number = list(map(Number, d.get('number',[])))
        else:
            finger = Finger('')
            number = list(map(Number, []))
        return cls(finger=finger, number=number)

    @property
    def ids(self):
        if len(self.number) == 0:
            return self.finger.ids
            
        return self.finger.char.replace('〇',self.number.char).replace('[','').replace(']','')

    def __str__(self) -> str:
        return str(self.finger) + ''.join(str(n) for n in self.number)

class Note(Element):
    """减字谱字的类
    """
    def __init__(self) -> None:
        raise NotImplementedError
    def __str__(self) -> str:
        raise NotImplementedError
    @classmethod
    def from_dict(self, d) -> None:
        assert isinstance(d, dict), f'input is not dict but of type {type(d)}'
        if 'simple_form' in d:
            return SimpleForm.from_dict(d['simple_form'])
        elif 'complex_form' in d:
            return ComplexForm.from_dict(d['complex_form'])
        elif 'aside_form' in d:
            return AsideForm.from_dict(d['aside_form'])
        elif 'marker' in d:
            return Marker(d['marker'])
    @property
    def ids(self, c=None):
        raise NotImplementedError
    @property
    def pitch(self, p=None):
        if p is None:
            try:
                xian = self.rightor.number_phrase.tokens
            except:
                xian = None
            try:
                hui = self.leftor.number_phrase.tokens
            except:
                hui = None
        # TODO
        raise NotImplementedError
@dataclass
class SimpleForm(Note):
    """简式谱字的类

    Attributes:
        hui_finger_phrase (FingerPhrase): 徽位指法短语
        xian_finger_phrase (FingerPhrase): 弦序指法短语
        special_finger (Finger): 特殊指法

    """
    hui_finger_phrase: FingerPhrase = None
    xian_finger_phrase: FingerPhrase = None
    special_finger: Finger = None

    @classmethod
    def from_dict(cls, d) -> None:
        hui_finger_phrase = FingerPhrase.from_dict(d.get('hui_finger_phrase'))
        xian_finger_phrase = FingerPhrase.from_dict(d.get('xian_finger_phrase'))
        special_finger = Finger(d.get('special_finger'))
        return cls(hui_finger_phrase=hui_finger_phrase, xian_finger_phrase=xian_finger_phrase, special_finger=special_finger)

    def __str__(self) -> str:
        return str(self.hui_finger_phrase)+ str(self.special_finger) + str(self.xian_finger_phrase)

@dataclass
class ComplexForm(Note):
    """复式谱字的类

    Attributes:
        complex_finger (Finger): 复式指法
        left_sub_phrase (SimpleForm): 左侧指法短语
        right_sub_phrase (SimpleForm): 右侧指法短语
    """
    complex_finger: Finger = None
    left_sub_phrase: SimpleForm = None
    right_sub_phrase: SimpleForm = None

    @classmethod
    def from_dict(cls, d) -> None:
        complex_finger = Finger(d['complex_finger'])
        left_sub_phrase = SimpleForm.from_dict(d['left_sub_phrase'])
        right_sub_phrase = SimpleForm.from_dict(d['right_sub_phrase'])
        return cls(complex_finger=complex_finger, left_sub_phrase=left_sub_phrase, right_sub_phrase=right_sub_phrase)

    def __str__(self) -> str:
        return str(self.complex_finger) + str(self.left_sub_phrase) + str(self.right_sub_phrase)

@dataclass
class AsideForm(Note):
    """旁字的类

    Attributes:
        modifier (Modifier): 修饰词
        special_finger (Finger): 特殊指法
        move_finger_phrase (FingerPhrase): 走位指法短语
    """
    modifier: Modifier = None
    special_finger: Finger = None
    move_finger_phrase: FingerPhrase = None

    @classmethod
    def from_dict(cls, d) -> None:
        modifier = Modifier(d.get('modifier'))
        special_finger = Finger(d.get('special_finger'))
        move_finger_phrase = FingerPhrase.from_dict(d.get('move_finger_phrase'))
        return cls(modifier=modifier, special_finger=special_finger, move_finger_phrase=move_finger_phrase)
    
    def __str__(self) -> str:
        return str(self.modifier) + str(self.special_finger) + str(self.move_finger_phrase)