from .constant import *
class Symbol():
    def __init__(self, name:str) -> None:
        self.name = name # 减字符号名称

    def __str__(self) -> str:
        return self.name

class Finger(Symbol):
    def __init__(self, name) -> None:
        super().__init__(name)
        self.valence = FINGERS.get(name, 0) # 价位，指法字配合的弦位字个数。譬如勾的价位为1，历的价位为2或3

class Number(Symbol):
    def __init__(self, name, value) -> None:
        super().__init__(name)
        self.value = value

class Modifier(Symbol):
    def __init__(self, name) -> None:
        super().__init__(name)

class Marker(Symbol):
    def __init__(self, name) -> None:
        super().__init__(name)

class Phrase():
    def __init__(self, finger: Finger, numbers: list[Number]):
        self.finger = finger
        assert len(numbers) == self.finger.valence, f'指法价位{self.finger.valence}与弦位或徽位数目{len(numbers)}不匹配'
        self.numbers = numbers

    def __str__(self) -> str:
        return str(self.finger)+ ''.join([str(number) for number in self.numbers])