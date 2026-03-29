from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

from .constants import (
    FORMS,
    PATH_TO_FIGMA,
    TAG,
    CN_from_EN,
    EN_from_CN,
    t_JIANZI,
    t_TAG,
)


@dataclass(frozen=True, slots=True)
class Area:
    x: float
    y: float
    width: float
    height: float

_EMPTY_AREA = Area(0, 0, 0, 0)

@dataclass
class LayoutNode:
    tag: t_TAG
    name: t_JIANZI
    area: Area
    children: dict[t_TAG, "LayoutNode"] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.name in CN_from_EN:
            self.name = CN_from_EN[self.name]
    
    def set_name(self, name:str):
        if name in CN_from_EN:
            self.name = CN_from_EN[name]
        else:
            self.name = name

    @property
    def name_en(self) -> str:
        return EN_from_CN[self.name]

    def is_leaf(self) -> bool:
        return not self.children

    def get_child(self, tag: t_TAG) -> "LayoutNode":
        return self.children[tag]

    def insert_child(self, child: "LayoutNode", tag: t_TAG) -> None:
        child_container = self.get_child(tag)
        child_container.children[child.tag] = child

    def flatten(self) -> list["LayoutNode"]:
        leaves: list["LayoutNode"] = []
        self._collect_leaves(offset_x=0, offset_y=0, leaves=leaves)
        return leaves

    def _collect_leaves(self, offset_x: float, offset_y: float, leaves: list["LayoutNode"]) -> None:
        for child in self.children.values():
            abs_x = offset_x + child.area.x
            abs_y = offset_y + child.area.y
            if child.is_leaf():
                child.area = Area(abs_x, abs_y, child.area.width, child.area.height)
                leaves.append(child)
            else:
                child._collect_leaves(abs_x, abs_y, leaves)
    
    # @classmethod
    # def from_dict(cls, d: dict) -> "LayoutNode":
    #     return
    
    # @classmethod
    # def from_layout(cls, layout: Layout) -> "LayoutNode":
    #     return

LayoutDict = dict[t_TAG, list[LayoutNode]]
@dataclass(frozen=True, slots=True)
class Component:
    name: t_JIANZI
    area: Area
    container_area: Area
    container_tag: t_TAG

ComponentDict = dict[t_JIANZI, Component]

def parse_figma(file: Path | str=PATH_TO_FIGMA):
    with open(file, "r", encoding="utf-8") as f:
        content = f.read()

    items = []
    for css_block in content.split("\n\n\n"):
        css_block = css_block.strip()
        css_lines = css_block.split("\n")
        name: str = css_lines.pop(0).split(" ")[1]
        kwargs: dict[str, float] = {}
        for line in css_lines:
            if line:
                key, value = line.strip().strip(";").split(": ")
                if value.endswith("px"):
                    value_ = float(value[:-2])
                    kwargs[key] = value_
        items.append((name, kwargs))
    # debug
    # return items

    layout_dict: LayoutDict = defaultdict(list)
    component_dict: dict[t_JIANZI, Component] = {}
    for i, item in enumerate(items):
        tag: t_TAG = item[0]
        area: dict = item[1]
        if tag.startswith("l_"):
            key = tag[2:]
            layout: LayoutNode = LayoutNode(tag=key, name="", area=_EMPTY_AREA)
            layout_dict[key].append(layout)
        elif tag in TAG:
            sublayout = LayoutNode(
                    tag=tag, name="", 
                    area=Area(
                    x=area["left"],
                    y=area["top"],
                    width=area["width"],
                    height=area["height"],
                )
            )
            layout.children[tag]=sublayout
        elif tag.startswith("c_"):
            # use temp key to not break the key for l_
            # store the component to the previous item
            component_name = tag[2:-3]
            last_tag: t_TAG = items[i-1][0]
            last_sublayout = layout.get_child(last_tag)
            last_sublayout.set_name(component_name)
            component_dict[component_name] = Component(
                name=component_name,
                area=Area(
                    x=area["left"],
                    y=area["top"],
                    width=area["width"],
                    height=area["height"],
                ),
                container_area=last_sublayout.area,
                container_tag=last_tag,
            )
    form_dict = {k: layout_dict.pop(k) for k in FORMS if k in layout_dict}
    return form_dict, layout_dict, component_dict
