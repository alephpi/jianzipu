from copyreg import constructor
from dataclasses import dataclass
from typing import Literal
from .constant import *


@dataclass
class Token():
    name: str
    def __str__(self) -> str:
        if not self.name:
            return ''
        return self.name

@dataclass
class Finger(Token):
    pass

@dataclass
class Number(Token):
    NUMBERS = {'一':1,'二':2,'三':3,'四':4,'五':5,'六':6,'七':7,'八':8,'九':9,'十':10,'十一':11,'十二':12,'十三':13,'半':5}
    pass
    # type: Literal['弦位','徽位'] 

@dataclass
class Modifier(Token):
    pass

@dataclass
class Marker(Token):
    pass

class Phrase():
    cls = None
    def __init__(self, tokens: list[str]) -> None:
        self.tokens =  None if tokens is None or tokens == [] else list(map(self.cls, tokens))

    def __str__(self) -> str:
        if not self.tokens:
            return ''
        return ''.join(str(token) for token in self.tokens)

class NumberPhrase(Phrase):
    cls = Number

class ModifierPhrase(Phrase):
    cls = Modifier
    
class FingerPhrase(Phrase):
    def __init__(self, finger:str, numbers:list[str]) -> None:
        self.finger = None if finger is None else Finger(finger)
        self.numbers =  None if numbers is None or numbers == [] else NumberPhrase(numbers)

    def __str__(self) -> str:
        return str(self.finger) + str(self.numbers)

class Note():
    def __init__(self, rightor:FingerPhrase, leftor:FingerPhrase, modifiers: ModifierPhrase, marker: Marker) -> None:
        self.rightor = rightor 
        self.leftor = leftor 
        self.modifiers = modifiers
        self.marker = marker

    def __str__(self) -> str:
        return str(self.leftor)+ str(self.modifiers) + str(self.rightor) + str(self.marker)