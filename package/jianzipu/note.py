from .parser import parse
from .symbol import Leftor, Rightor, Bothor, Marker, Xian, Hui, Fen

class Note():
    def __init__(self,
                 rightor: Rightor|None,
                 leftor: Leftor|None,
                 xian: Xian|None,
                 hui: Hui|None,
                 fen: Fen|None,
                 modifiers: list[str]) -> None:
        self.rightor = rightor
        self.leftor = leftor
        self.xian = xian
        self.hui = hui
        self.fen = fen
        self.modifiers = modifiers

    @classmethod
    def from_parsing(cls, s):
        d = parse(s)
        return cls(**d)