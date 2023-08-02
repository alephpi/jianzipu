from .symbol import Finger, Modifier, Marker 

class Note():
    def __init__(self,
                 rightor: Finger|None,
                 leftor: Finger|None,
                 bothor: Finger|None,
                 modifiers: list[Modifier]|None,
                 marker: Marker) -> None:

        self.rightor = rightor
        self.leftor = leftor
        self.modifiers = modifiers
        self.marker = marker

    def __str__(self) -> str:
        return str(self.leftor)+ ''.join([str(i) for i in self.modifiers]) + str(self.rightor) + ''.join([str(i) for i in self.marker])