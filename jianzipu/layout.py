from collections import defaultdict
from copy import deepcopy
from dataclasses import dataclass, field
from itertools import product
from pathlib import Path

from .constants import (
    CHILDREN_TAGS_ORDER_INDEX,
    FORMS,
    GLYPH_ORDER,
    GLYPHS,
    PATH_TO_FIGMA,
    REDUCED_FROM_FULL,
    TAG,
    CN_from_EN,
    EN_from_CN,
    t_FORM,
    t_JIANZI,
    t_TAG,
)


@dataclass(frozen=True, slots=True)
class Area:
    x: int
    y: int
    width: int
    height: int

    @property
    def xywh(self):
        return self.x, self.y, self.width, self.height

_EMPTY_AREA = Area(0, 0, 0, 0)

@dataclass
class LayoutNode:
    tag: t_TAG
    name: t_JIANZI
    area: Area
    children: dict[t_TAG, "LayoutNode"] = field(default_factory=dict)

    def __rich_repr__(self):
        yield "tag", self.tag
        if self.name:
            yield "name", self.name
        if self.area != _EMPTY_AREA:
            yield "area", self.area
        if self.children:
            yield "children", self.children

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

    def get_children_tags(self):
        return self.children.keys()

    def get_child_of_tag(self, tag: t_TAG) -> "LayoutNode":
        return self.children[tag]

    def _sort_children(self) -> None:
        """reorder children according to the order defined in CHILDREN_TAGS_ORDER_INDEX, 
        so that the flattened tree preserves the syntax order.
        """
        order_index = CHILDREN_TAGS_ORDER_INDEX.get(self.tag)
        if not order_index:
            return
        self.children = dict(
            sorted(self.children.items(), key=lambda item: order_index[item[0]])
        )

    def set_child(self, child: "LayoutNode") -> None:
        order_index = CHILDREN_TAGS_ORDER_INDEX.get(self.tag)
        if order_index is not None and child.tag not in order_index:
            raise ValueError(f"Invalid child tag {child.tag} for parent {self.tag}")
        self.children[child.tag] = child
        self._sort_children()
    
    def fill_child(self, child: "LayoutNode") -> None:
        order_index = CHILDREN_TAGS_ORDER_INDEX.get(self.tag)
        if order_index is not None and child.tag not in order_index:
            raise ValueError(f"Invalid child tag {child.tag} for parent {self.tag}")
        old_child = self.children[child.tag]
        # if not old_child:
        #     raise ValueError(f"Tag {child.tag} not found in template {self}, check the figma.css file if you correctly output the layout templates")
        child.area = old_child.area
        self.children[child.tag] = child
        self._sort_children()
 
    def flatten(self) -> "LayoutNode":
        """return a new LayoutNode with the same leaves but flattened structure"""
        leaves: list["LayoutNode"] = []
        self._collect_leaves(offset_x=0, offset_y=0, leaves=leaves)
        flattened = LayoutNode(
                        tag=self.tag,
                        name=self.name,
                        area=self.area,
                        children={leave.tag: leave for leave in leaves}
                        )
        return flattened

    def _collect_leaves(self, offset_x: float, offset_y: float, leaves: list["LayoutNode"]) -> None:
        for child in self.children.values():
            abs_x = offset_x + child.area.x
            abs_y = offset_y + child.area.y
            if child.is_leaf():
                leaf = LayoutNode(
                    tag=child.tag,
                    name=child.name,
                    area=Area(abs_x, abs_y, child.area.width, child.area.height),
                    children={},
                )
                leaves.append(leaf)
            else:
                child._collect_leaves(abs_x, abs_y, leaves)

@dataclass(frozen=True, slots=True)
class Component:
    name: t_JIANZI
    area: Area
    container_area: Area
    container_tag: t_TAG

    @property
    def xywh(self):
        return self.area.xywh

def parse_figma(file: Path | str=PATH_TO_FIGMA) -> tuple[dict[t_FORM, list[LayoutNode]], dict[t_TAG, list[LayoutNode]], dict[t_JIANZI, Component]]:
    """
    Parse the figma.css file to get the form_templates, layout templates and component dict.
    """
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

    layout_templates: dict[t_TAG, list[LayoutNode]] = defaultdict(list)
    component_dict: dict[t_JIANZI, Component] = {}
    for i, item in enumerate(items):
        tag: t_TAG = item[0]
        area: dict = item[1]
        if tag.startswith("l_"):
            key = tag[2:]
            # l_ 开头说明是布局或子布局的模板，若为布局（即form）则是根节点，area是(0,0,1000,1000)即标准字形框。而若为子布局，则area_filler为空，待填入其他布局的子节点时才会有具体的数值
            if key in FORMS:
                area_filler = Area(0, 0, 1000, 1000)
            else:
                area_filler = Area(0, 0, round(area["width"]), round(area["height"]))
            layout: LayoutNode = LayoutNode(tag=key, name="", area=area_filler)
            layout_templates[key].append(layout)
        elif tag in TAG:
            sublayout = LayoutNode(
                    tag=tag, name="", 
                    area=Area(
                    x=round(area["left"]),
                    y=round(area["top"]),
                    width=round(area["width"]),
                    height=round(area["height"]),
                )
            )
            layout.set_child(sublayout)
        elif tag.startswith("c_"):
            # component name format is c_{glyphName}.{variantName}, e.g. c_tuo1.sm, c_tuo1.md, c_tuo1.lg
            component_name = tag[2:]
            # store the component to the predecessor sublayout
            last_tag: t_TAG = items[i-1][0]
            if last_tag.startswith("l_"):
                last_layout = layout
                last_tag = last_tag[2:]
            else:
                last_layout = layout.get_child_of_tag(last_tag)
                # use the component name without variant suffix in the sublayout
            last_layout.set_name(component_name.split(".")[0])
            component_dict[component_name] = Component(
                name=component_name,
                area=Area(
                    x=round(area["left"]),
                    y=round(area["top"]),
                    width=round(area["width"]),
                    height=round(area["height"]),
                ),
                container_area=last_layout.area,
                container_tag=last_tag,
            )
    full_form_templates: dict[t_FORM, list[LayoutNode]] = {k: layout_templates.pop(k) for k in FORMS if k in layout_templates}

    # generate reduced form from full form according to REDUCED_FROM_FULL_FORM
    all_form_templates = deepcopy(full_form_templates)
    for k_form, full_forms in full_form_templates.items():
        for full_form in full_forms:
            full_children_tags = tuple(full_form.get_children_tags())
            reduced_children_tags_l = REDUCED_FROM_FULL.get(full_children_tags, [])
            for reduced_children_tags in reduced_children_tags_l:
                reduced_form = deepcopy(full_form)
                reduced_form.children = {
                    tag: child
                    for tag, child in reduced_form.children.items()
                    if tag in reduced_children_tags
                }
                all_form_templates[k_form].append(reduced_form)
    
    # generate reduced layout from full layout according to REDUCED_FROM_FULL
    all_layout_templates = deepcopy(layout_templates)
    for k_layout, full_layouts in layout_templates.items():
        for full_layout in full_layouts:
            full_children_tags = tuple(full_layout.get_children_tags())
            reduced_children_tags_l = REDUCED_FROM_FULL.get(full_children_tags, [])
            for reduced_children_tags in reduced_children_tags_l:
                reduced_layout = deepcopy(full_layout)
                reduced_layout.children = {
                    tag: child
                    for tag, child in reduced_layout.children.items()
                    if tag in reduced_children_tags
                }
                all_layout_templates[k_layout].append(reduced_layout)

    component_dict = dict(sorted(component_dict.items(), key=lambda item: GLYPH_ORDER.get(item[0], float('inf'))))
    return all_form_templates, all_layout_templates, component_dict

def get_all_layouts(form_templates: dict[t_FORM, list[LayoutNode]], layout_templates: dict[t_TAG, list[LayoutNode]], flatten: bool) -> list[LayoutNode]:
    """Get all possible layouts by injecting layout templates into form templates
    """
    all_layouts: list[LayoutNode] = []
    for form_layouts in form_templates.values():
        for form_layout in form_layouts:
            tags: list[t_TAG] = [tag for tag in form_layout.get_children_tags() if tag in layout_templates]
            layout_options = [layout_templates[tag] for tag in tags]
            for layouts in product(*layout_options):
                combined = deepcopy(form_layout)
                for layout in layouts:
                    combined.fill_child(deepcopy(layout))
                all_layouts.append(combined.flatten() if flatten else combined)
    return all_layouts