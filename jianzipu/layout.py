from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

from .constant import TAG, t_JIANZI, t_TAG


@dataclass(frozen=True, slots=True)
class Area:
    x: float
    y: float
    width: float
    height: float

_EMPTY_AREA = Area(0, 0, 0, 0)

@dataclass(frozen=True, slots=True)
class LayoutItem:
    tags: list[t_TAG]
    values: list[t_JIANZI]
    areas: list[Area]

@dataclass(frozen=True, slots=True)
class Component:
    name: str
    area: Area
    container_tag: t_TAG


Layout = dict[t_TAG, list[LayoutItem]]


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

def parse_figma_to_layout(file: Path | str):
    with open(file, "r", encoding="utf-8") as f:
            content = f.read()

    # layouts: list[Layout] = []
    items = []
    for css_block in content.split("\n\n\n"):
        css_block = css_block.strip()
        css_lines = css_block.split("\n")
        name = css_lines.pop(0).split(" ")[1]
        kwargs: dict[str, float] = {}
        for line in css_lines:
            if line:
                key, value = line.strip().strip(";").split(": ")
                if value.endswith("px"):
                    value_ = float(value[:-2])
                    kwargs[key] = value_
        items.append((name, kwargs))
    # return items

    layout: Layout = defaultdict(list)
    components: dict[str, Component] = {}
    for i, item in enumerate(items):
        name: str = item[0]
        area: dict = item[1]
        if name.startswith("l_"):
            key = name[2:]
            layout_item: LayoutItem = LayoutItem(tags=[], values=[], areas=[])
            layout[key].append(layout_item)
        elif name in TAG:
            if layout_item:
                layout_item.tags.append(name)
                layout_item.values.append("")
                layout_item.areas.append(
                    Area(
                        x=area["left"],
                        y=area["top"],
                        width=area["width"],
                        height=area["height"],
                    )
                )
        elif name.startswith("c_"):
            # use temp key to not break the key for l_
            # store the component to the previous item
            component_name = name[2:]
            layout_item.values[-1] = component_name
            components[component_name] = Component(
                name=component_name,
                area=Area(
                    x=area["left"],
                    y=area["top"],
                    width=area["width"],
                    height=area["height"],
                ),
                container_tag=items[i - 1],
            )
    return layout, components

    # def insert_child(self, child: "ParseNode", index: Optional[int] = None) -> None:
    #     if index is None:
    #         self.children.append(child)
    #     else:
    #         self.children.insert(index, child)

    # def flatten(self) -> None:
    #     leaves: List["ParseNode"] = []
    #     self._collect_leaves(offset_x=0, offset_y=0, leaves=leaves)
    #     self.children = leaves

    # def _collect_leaves(self, offset_x: float, offset_y: float, leaves: List["ParseNode"]) -> None:
    #     for child in self.children:
    #         abs_x = offset_x + child.area.x
    #         abs_y = offset_y + child.area.y
    #         if child.is_leaf():
    #             child.area = Area(abs_x, abs_y, child.area.width, child.area.height)
    #             leaves.append(child)
    #         else:
    #             child._collect_leaves(abs_x, abs_y, leaves)