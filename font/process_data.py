import json
from typing import TypedDict

import font


def parse_number_layout(file="./layouts/number.txt") -> list[font.Component]:
    with open(file, "r", encoding="utf-8") as f:
        content = f.read()

    components: list[font.Component] = []
    for css_block in content.split("\n\n\n"):
        css_block = css_block.strip()
        css_lines = css_block.split("\n")
        name = css_lines.pop(0).split(" ")[1]
        if name.startswith("n"):
            kwargs = {}
            for line in css_lines:
                if line:
                    key, value = line.strip().strip(";").split(": ")
                    if value.endswith("px"):
                        value = float(value[:-2])
                    kwargs[key] = value
            component = font.Component(
                name=name,
                svg_path=f"./components/{name}.svg",
                width=kwargs["width"],
                height=kwargs["height"],
                relative=font.Position(x=kwargs["left"], y=kwargs["top"]),
            )
            components.append(component)
    components.sort(key=lambda x: x.name)

    return components

def parse_hui_finger_layout(file="./layouts/hui_finger.txt") -> list[font.Component]:
    with open(file, "r", encoding="utf-8") as f:
        content = f.read()

    components: list[font.Component] = []
    for css_block in content.split("\n\n\n"):
        css_block = css_block.strip()
        css_lines = css_block.split("\n")
        name = css_lines.pop(0).split(" ")[1]
        if name.startswith("c_h"):
            kwargs = {}
            for line in css_lines:
                if line:
                    key, value = line.strip().strip(";").split(": ")
                    if value.endswith("px"):
                        value = float(value[:-2])
                    kwargs[key] = value
            component = font.Component(
                name=name,
                svg_path=f"./components/{name[2:]}.svg",
                width=kwargs["width"],
                height=kwargs["height"],
                relative=font.Position(x=kwargs["left"], y=kwargs["top"]),
            )
            components.append(component)
    components.sort(key=lambda x: x.name)

    return components

def parse_xian_finger_layout(file="./layouts/xian_finger.txt") -> list[font.Frame]:
    with open(file, "r", encoding="utf-8") as f:
        content = f.read()

    layouts: list[font.Frame] = []
    for css_block in content.split("\n\n\n"):
        css_block = css_block.strip()
        css_lines = css_block.split("\n")
        name = css_lines.pop(0).split(" ")[1]
        if name.startswith("l_x"):
            kwargs = {}
            for line in css_lines:
                if line:
                    key, value = line.strip().strip(";").split(": ")
                    if value.endswith("px"):
                        value = float(value[:-2])
                    kwargs[key] = value
            layout = font.FingerLayout(
                name=name,
                width=kwargs["width"],
                height=kwargs["height"],
            )

        elif name.startswith("c_x"):
            kwargs = {}
            for line in css_lines:
                if line:
                    key, value = line.strip().strip(";").split(": ")
                    if value.endswith("px"):
                        value = float(value[:-2])
                    kwargs[key] = value
            component = font.Component(
                name=name,
                svg_path=f"./components/{name[2:]}.svg",
                width=kwargs["width"],
                height=kwargs["height"],
                relative=font.Position(x=kwargs["left"], y=kwargs["top"]),
            )
            layout.children.append(component)
        elif name == "n_placeholder":
            kwargs = {}
            for line in css_lines:
                if line:
                    key, value = line.strip().strip(";").split(": ")
                    if value.endswith("px"):
                        value = float(value[:-2])
                    kwargs[key] = value
            component = font.Placeholder(
                name=name,
                width=kwargs["width"],
                height=kwargs["height"],
                relative=font.Position(x=kwargs["left"], y=kwargs["top"]),
            )
            layout.placeholders.append(component)
        else:
            raise ValueError(f"Unknown name: {name}")
        layouts.append(layout)


    return layouts





def main():
    components = parse_number_layout()
    with open("./jsons/number.json", "w", encoding="utf-8") as f:
        json.dump(
            [component.model_dump() for component in components],
            f,
            ensure_ascii=False,
            indent=2,
        )

if __name__ == "__main__":
    main()