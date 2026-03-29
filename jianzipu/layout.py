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

@dataclass(frozen=True, slots=True)
class Layout:
    tags: list[t_TAG]
    names: list[t_JIANZI]
    areas: list[Area]

LayoutDict = dict[t_TAG, list[Layout]]
@dataclass(frozen=True, slots=True)
class Component:
    name: str
    area: Area
    container_area: Area
    container_tag: t_TAG

ComponentDict = dict[str, Component]


# t_TAGS = tuple[t_TAG, ...]
# t_VALUES = tuple[t_JIANZI, ...]
# t_AREAS = tuple[Area, ...]

# t_LAYOUT = dict[tuple[t_TAGS, t_VALUES], t_AREAS]
# t_LAYOUTS = dict[t_TAG, t_LAYOUT]

# LAYOUTS: t_LAYOUTS = {
#     "hfp": {
#     (("hf",), ("",)): (Area(0, 0, 100, 40),),
#     (("hf", "hn1"), ("", "")): (Area(0, 0, 60, 40), Area(65, 0, 60, 40)),
#     (("hf", "hn1", "hn2"), ("", "", "")): (Area(0, 0, 60, 40), Area(65, 0, 60, 40), Area(130, 0, 60, 40))
#     },
#     "xfp": {
#     (("xf",), ("",)): (Area(0, 0, 100, 40),),
#     (("xf", "xn1"), ("", "")): (Area(0, 0, 60, 40), Area(65, 0, 60, 40)),
#     (("xf", "xn1", "xn2"), ("", "", "")): (Area(0, 0, 60, 40), Area(65, 0, 60, 40), Area(130, 0, 60, 40)),
#     }
# }

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
    component_dict: dict[str, Component] = {}
    for i, item in enumerate(items):
        tag: t_TAG = item[0]
        area: dict = item[1]
        if tag.startswith("l_"):
            key = tag[2:]
            layout: Layout = Layout(tags=[], names=[], areas=[])
            layout_dict[key].append(layout)
        elif tag in TAG:
            if layout:
                layout.tags.append(tag)
                layout.names.append("")
                layout.areas.append(
                    Area(
                        x=area["left"],
                        y=area["top"],
                        width=area["width"],
                        height=area["height"],
                    )
                )
        elif tag.startswith("c_"):
            # use temp key to not break the key for l_
            # store the component to the previous item
            component_name = tag[2:-3]
            layout.names[-1] = component_name
            component_dict[component_name] = Component(
                name=component_name,
                area=Area(
                    x=area["left"],
                    y=area["top"],
                    width=area["width"],
                    height=area["height"],
                ),
                container_area=layout.areas[-1],
                container_tag=layout.tags[-1],
            )
    form_dict = {k: layout_dict.pop(k) for k in FORMS if k in layout_dict}
    return form_dict, layout_dict, component_dict

# FORM_DICT, LAYOUT_DICT, COMPONENT_DICT = parse_figma_to_layout(PATH_TO_FIGMA)


@dataclass
class LayoutNode:
    tag: str
    name: str
    area: Area
    children: dict[str, "LayoutNode"] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.name in CN_from_EN:
            self.name = CN_from_EN[self.name]

    @property
    def name_en(self) -> str:
        return EN_from_CN[self.name]

    def is_leaf(self) -> bool:
        return not self.children

    def get_child(self, tag: str) -> "LayoutNode":
        return self.children[tag]

    def insert_child(self, child: "LayoutNode", tag: str) -> None:
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
    
    @classmethod
    def from_dict(cls, d: dict) -> "LayoutNode":
        return
    
    @classmethod
    def from_layout(cls, layout: Layout) -> "LayoutNode":
        return