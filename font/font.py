from typing import Any, List, Optional, Union

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
    filled: List[Component] = Field(default_factory=list)
    components: List[Component] = Field(default_factory=list)

    def model_post_init(self, __context: Any) -> None:
        self.filled = [None] * len(self.placeholders)

    def posit(self, reference: Position = Position()) -> None:
        for child in self.children:
            if isinstance(child, Component):
                child.absolute = reference + child.relative
            else:
                child.absolute = reference + child.relative
                child.posit(child.absolute)
        for filled in self.filled:
            filled.absolute = reference + filled.relative

    # return all the components in the frame, flattened
    def flatten(self) -> List[Component]:
        components: List[Component] = []
        for child in self.children:
            if isinstance(child, Component):
                components.append(child)
            else:
                components.extend(child.flatten())
        components.extend(self.filled)
        return components
    
    def fill_placeholder(self, component: Component, idx: int) -> None:
        assert idx < len(self.placeholders)
        component_copy = component.model_copy(deep=True)
        scale = self.placeholders[idx].width / component_copy.width, self.placeholders[idx].height/ component_copy.height
        component_copy.relative = scale * component_copy.relative + self.placeholders[idx].relative # put component at the position of placeholder, i.e. from relative to the placeholder to relative to the frame
        component_copy.relative.x = round(component_copy.relative.x, 2)
        component_copy.relative.y = round(component_copy.relative.y, 2)
        self.filled[idx] = component_copy

    model_config = {
        "arbitrary_types_allowed": True
    }


class FingerLayout(Frame):
    ...

class BigSizedLayout(Frame):
    ...