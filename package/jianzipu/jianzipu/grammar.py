from abc import ABC, abstractmethod
from dataclasses import dataclass
from functools import reduce

from .constant import JIANZI
from .ids import IDS
from .kage import Kage

class Element(ABC):
    """减字谱语法基本元素抽象类"""

    @abstractmethod
    def __str__(self) -> str:
        """返回对应的读法
        """
        raise NotImplementedError
    
    @abstractmethod
    def draw(self, font='serif'):
        raise NotImplementedError

class Empty(Element):
    def __str__(self) -> str:
        return ''
    @property
    def char(self) -> str:
        return ''
    @property
    def kage(self):
        return None
    def draw(self, font='serif'):
        pass

Null = Empty()

@dataclass
class Symbol(Element):
    """减字符号

    Attributes:
        id (str): 减字符号的名称
        char (str): 减字符号的字面形式（文字或表意文字描述序列）
    """
    id: str = ''
    def __post_init__(self) -> None:
        self.char = IDS(JIANZI.get(self.id, ''))

    def __str__(self) -> str:
        if self.id is None:
            return ''
        return self.id
    
    @property
    def kage(self) -> Kage:
        return Kage.primitive(self.id)
    
    def draw(self, font='serif'):
        # self.char.draw()
        return self.kage.draw(font=font)

@dataclass
class Finger(Symbol):
    """指法符号
    """
    pass
@dataclass
class Number(Symbol):
    """数字符号
    """
    def __post_init__(self) -> None:
        self._key = self.id.replace('弦','').replace('徽','').replace('分','')
        self.char = IDS(JIANZI[self._key])

    @property
    def kage(self):
        return Kage.primitive(self._key)
@dataclass
class Modifier(Symbol):
    """修饰符号
    """
    pass

@dataclass
class Marker(Symbol):
    """标记符号
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

class NumberPhrase(list[Number]):
    def __init__(self, args: list[Number]):
        if isinstance(args, list) & all(isinstance(arg, Number) for arg in args):
            super().__init__(args)
        else:
            raise TypeError("Number phrase should be a list of Number")

    def __str__(self) -> str:
        return ''.join(str(n) for n in self)

    def __repr__(self) -> str:
        return f"[{','.join(repr(n) for n in self)}]"

    @property
    def char(self) -> IDS:
        return reduce(IDS.__add__, (n.char for n in self))
    
    @property
    def kage(self) -> Kage:
        if len(self) == 0:
            return Kage()
        elif len(self) == 1:
            return self[0].kage
        elif len(self) == 2:
            return Kage.top_bottom(top=self[0].kage, bottom=self[1].kage, kind='number')
        else:
            raise Exception(f"Number phrase should have at most 2 elements, got {len(self)}")

    def draw(self, font='serif'):
        # return self.char.draw()
        return self.kage.draw(font=font)
    

# class ModifierPhrase(Phrase):
#     cls = Modifier

@dataclass
class FingerPhrase(Element):
    """指法短语

    Attributes:
        finger (Finger): 指法符号
        number (list[Number]): 数字符号列表

    """
    finger: Finger = Null 
    number: NumberPhrase = Null

    @classmethod
    def from_dict(cls, d) -> None:
        if isinstance(d, dict):
            finger = Finger(d.get('finger',''))
            number = NumberPhrase(list(map(Number, d.get('number',[]))))
        else:
            finger = Null
            number = Null
        return cls(finger=finger, number=number)

    @property
    def char(self):
        if len(self.number) == 0:
            return self.finger.char
        return self.finger.char * self.number.char
    
    @property
    def kage(self):
        a = self.finger is not Null
        b = self.number is not Null
        match a,b:
            case True, False:
                return self.finger.kage
            case False, True:
                return self.number.kage
            case True, True:
                return Kage.finger_phrase(self.finger.kage, self.number.kage)

    def draw(self, font='serif'):
        # self.char.draw()
        return self.kage.draw(font=font)

    def __str__(self) -> str:
        return str(self.finger) + str(self.number)

class Note(Element):
    """谱字
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
    def char(self):
        raise NotImplementedError
    
    @property
    def kage(self):
        raise NotImplementedError

    def draw(self, font='serif'):
        # return self.char.draw()
        return self.kage.draw(font=font)
    # @property
    # def pitch(self, p=None):
    #     if p is None:
    #         try:
    #             xian = self.rightor.number_phrase.tokens
    #         except:
    #             xian = None
    #         try:
    #             hui = self.leftor.number_phrase.tokens
    #         except:
    #             hui = None
    #     # TODO
    #     raise NotImplementedError
@dataclass
class SimpleForm(Note):
    """简式谱字

    Attributes:
        hui_finger_phrase (FingerPhrase): 徽位指法短语
        xian_finger_phrase (FingerPhrase): 弦序指法短语
        special_finger (Finger): 特殊指法

    """
    hui_finger_phrase: FingerPhrase = Null
    xian_finger_phrase: FingerPhrase = Null
    special_finger: Finger = Null

    @classmethod
    def from_dict(cls, d) -> None:
        hui_finger_phrase = FingerPhrase.from_dict(d.get('hui_finger_phrase'))
        xian_finger_phrase = FingerPhrase.from_dict(d.get('xian_finger_phrase'))
        special_finger = Finger(d.get('special_finger'))
        return cls(hui_finger_phrase=hui_finger_phrase, xian_finger_phrase=xian_finger_phrase, special_finger=special_finger)

    @property
    def char(self):
        return self.hui_finger_phrase.char + self.special_finger.char * self.xian_finger_phrase.char

    @property
    def kage(self):
        hui_finger_phrase_kage = self.hui_finger_phrase.kage
        xian_finger_phrase_kage = self.xian_finger_phrase.kage
        special_finger_kage = self.special_finger.kage
        return Kage.simple_form(hui_finger_phrase_kage, xian_finger_phrase_kage, special_finger_kage)

    def __str__(self) -> str:
        return str(self.hui_finger_phrase) + str(self.special_finger) + str(self.xian_finger_phrase)

@dataclass
class ComplexForm(Note):
    """复式谱字

    Attributes:
        complex_finger (Finger): 复式指法
        left_sub_phrase (SimpleForm): 左侧指法短语
        right_sub_phrase (SimpleForm): 右侧指法短语
    """
    complex_finger: Finger = Null
    left_sub_phrase: SimpleForm = Null
    right_sub_phrase: SimpleForm = Null

    @classmethod
    def from_dict(cls, d) -> None:
        complex_finger = Finger(d['complex_finger'])
        left_sub_phrase = SimpleForm.from_dict(d['left_sub_phrase'])
        right_sub_phrase = SimpleForm.from_dict(d['right_sub_phrase'])
        return cls(complex_finger=complex_finger, left_sub_phrase=left_sub_phrase, right_sub_phrase=right_sub_phrase)
    
    @property
    def char(self):
        # TODO
        return IDS('⿱⿰正在⿰施工')
    
    def draw(self, font='serif'):
        self.char.draw(font=font)

    def __str__(self) -> str:
        return str(self.complex_finger) + str(self.left_sub_phrase) + str(self.right_sub_phrase)

@dataclass
class AsideForm(Note):
    """旁字

    Attributes:
        modifier (Modifier): 修饰词
        special_finger (Finger): 特殊指法
        move_finger_phrase (FingerPhrase): 走位指法短语
    """
    modifier: Modifier = Null
    special_finger: Finger = Null
    move_finger_phrase: FingerPhrase = Null

    @classmethod
    def from_dict(cls, d) -> None:
        modifier = Modifier(d.get('modifier'))
        special_finger = Finger(d.get('special_finger'))
        move_finger_phrase = FingerPhrase.from_dict(d.get('move_finger_phrase'))
        return cls(modifier=modifier, special_finger=special_finger, move_finger_phrase=move_finger_phrase)
    
    @property
    def char(self):
        return self.modifier.char + self.special_finger.char * self.move_finger_phrase.char
    
    def draw(self, font='serif'):
        self.char.draw(font=font)

    def __str__(self) -> str:
        return str(self.modifier) + str(self.special_finger) + str(self.move_finger_phrase)