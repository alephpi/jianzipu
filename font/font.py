from typing import List, Optional, Union

from pydantic import BaseModel, Field


class Position(BaseModel):
    x: float = 0.0
    y: float = 0.0
    
    def add(self, other: "Position") -> "Position":
        return Position(x=self.x + other.x, y=self.y + other.y)
    
    def __add__(self, other: "Position") -> "Position":
        return self.add(other)
    
    def scale(self, other: tuple[float, float]) -> "Position":
        return Position(x=self.x * other[0], y=self.y * other[1])
    
    def __mul__(self, other: tuple[float, float]) -> "Position":
        return self.scale(other)
    
    def __rmul__(self, other: tuple[float, float]) -> "Position":
        return self.scale(other)


class Component(BaseModel):
    name: str
    svg_path: str
    width: float
    height: float
    relative: Position = Field(default_factory=Position)
    absolute: Optional[Position] = None

class Placeholder(BaseModel):
    name: str
    width: float
    height: float
    relative: Position = Field(default_factory=Position)

class Frame(BaseModel):
    name: str
    width: float
    height: float
    relative: Position = Field(default_factory=Position)
    absolute: Optional[Position] = None
    children: List[Union["Frame", Component]] = Field(default_factory=list)
    placeholders: List[Placeholder] = Field(default_factory=list)

    def posit(self, reference: Position = Position()) -> None:
        for child in self.children:
            if isinstance(child, Component):
                child.absolute = reference + child.relative
            else:
                child.absolute = reference + child.relative
                child.posit(child.absolute)
    
    def flatten(self) -> List[Component]:
        components: List[Component] = []
        for child in self.children:
            if isinstance(child, Component):
                components.append(child)
            else:
                components.extend(child.flatten())
        return components
    
    def fill_placeholder(self, component: Component, idx: int) -> None:
        assert idx < len(self.placeholders)
        scale = component.width / self.placeholders[idx].width, component.height / self.placeholders[idx].height
        component.relative = scale * component.relative + self.placeholders[idx].relative # put component at the position of placeholder, i.e. from relative to the placeholder to relative to the frame
        self.children.append(component)

    model_config = {
        "arbitrary_types_allowed": True
    }


class FingerLayout(Frame):
    ...

class BigSizedLayout(Frame):
    ...