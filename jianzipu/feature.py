import yaml

from .constants import PATH_TO_FEA, PATH_TO_FEATURES
from .layout import LayoutNode
from .parser import ParseNode


def import_features(file=PATH_TO_FEATURES):
    with open(file, "r") as f:
        features = yaml.safe_load(f)
        macros = {}
        rule_templates = {}
        for k, v in features.items():
            if k.startswith("@"):
                macros[k] = v
            else:
                rule_templates[tuple(k.split(" "))] = v
    return macros, rule_templates

def write_macros(macros):
    lines = []
    for key, value in macros.items():
        if isinstance(value, list):
            line = f"{key}=[{' '.join(value)}];"
        else:
            line = f"{key}={value};"
        lines.append(line)
    fea_text = "\n".join(lines)
    return fea_text

def write_rule_templates(layout: LayoutNode, rule_templates: dict[tuple[str, ...], str]):
    tags = tuple(layout.get_children_tags())
    rule_template = rule_templates[tags]
    rule = []
    for node, term in zip(layout.children.values(), rule_template):
        if node.name == "":
            x, y = node.area.x, node.area.y
            rule.append(f"{term}' <{x} {y} 0 0>")
        else:
            rule.append(f"{node.name_en}.{term[-2:]}' <{node.area.x} {node.area.y} 0 0>")
    return "pos " + " ".join(rule)

def write_fea(macros, rule_templates, fea_path=PATH_TO_FEA):
    with open(fea_path, "w") as f:
        f.write(write_macros(macros))
        # TODO write rule templates

def find_matching_layout(puzi: ParseNode, all_layouts: list[LayoutNode]):
    """Return all layouts matching a parse tree.

    Match rules:
    1) parse_tree tags must be a subset of layout tags.
    2) For each jianzi in parse_tree, layout name is wildcard when "",
       otherwise it must equal jianzi.name.
    """
    puzi_tag_set = set(puzi.get_children_tags())
    matched_layouts: list[LayoutNode] = []

    for layout in all_layouts:
        layout_tag_set = set(layout.get_children_tags())
        if not puzi_tag_set.issubset(layout_tag_set):
            continue

        if all(
            layout.children[jianzi.tag].name == ""
            or layout.children[jianzi.tag].name == jianzi.name
            for jianzi in puzi.children.values()
        ):
            matched_layouts.append(layout)

    if not matched_layouts:
        raise ValueError("No matching layout found, have you implemented in figma.css?")

    return next(
        (layout for layout in matched_layouts if set(layout.get_children_tags()) == puzi_tag_set),
        matched_layouts[0],
    )

if __name__ == "__main__":
    macros, rule_templates = import_features()
    write_fea(macros, rule_templates)