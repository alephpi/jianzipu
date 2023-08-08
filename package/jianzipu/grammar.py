from dataclasses import dataclass, field
import re

from .constant import JIANZI


@dataclass
class Token:
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
class Finger(Token):
    pass
@dataclass
class Number(Token):
    def __post_init__(self) -> None:
        key = self.id.replace('弦','').replace('徽','').replace('分','')
        self.char = JIANZI[key]

@dataclass
class Modifier(Token):
    pass

@dataclass
class Marker(Token):
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
class FingerPhrase():
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
        if self.number == []:
            pass
        return self.finger.char.replace('〇',self.number.char).replace('[','').replace(']','')

    def __str__(self) -> str:
        return str(self.finger) + ''.join(str(n) for n in self.number)

class Note:
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