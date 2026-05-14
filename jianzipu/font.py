from pathlib import Path

import ufo2ft
import ufoLib2
from fontTools.misc.transform import Transform
from fontTools.pens.pointPen import SegmentToPointPen
from fontTools.pens.roundingPen import RoundingPointPen
from fontTools.svgLib import SVGPath

from .constants import PATH_TO_FEA, PATH_TO_FONT, PATH_TO_SVGS
from .layout import parse_figma
from .metadata import METADATA

PATH_TO_UFO = PATH_TO_FONT / Path(METADATA.fontname).with_suffix('.ufo')
PATH_TO_TTF = PATH_TO_FONT / Path(METADATA.fontname).with_suffix('.ttf')

def init(font: ufoLib2.Font):
    info = font.info

    # postscript 名（无空格）
    info.postscriptFontName = METADATA.fontname

    # 版权 / 许可
    info.copyright = METADATA.copyright
    info.openTypeNameLicense = METADATA.license
    info.openTypeNameLicenseURL = METADATA.license_url

    # 设计师
    info.openTypeNameDesigner = METADATA.designer
    info.openTypeNameDesignerURL = METADATA.designer_url

    # 版本：拆成 major / minor（必须是 int）
    major, minor, _ = METADATA.version.split(".")
    info.versionMajor = int(major)
    info.versionMinor = int(minor)

    # 顺带设置 family / style name
    info.familyName = METADATA.fontname
    info.styleName  = "Regular"

    # .notdef
    notdef = font.newGlyph(".notdef")
    notdef.width = 0

    glyph = font.newGlyph("space")
    glyph.width = 500
    glyph.unicode = 0x0020

def make_glyph_from_components(font: ufoLib2.Font, rounding = True):
    _, _, component_dict = parse_figma()
    for name, component in component_dict.items():
        svg_path = PATH_TO_SVGS / f"c_{name}.svg"
        with open(svg_path, "r", encoding="utf-8") as f:
            svg_content = f.read()
        x, y, w, h = component.xywh
        # transform from svg coordinate system (y down) to font coordinate system (y up)
        transform = Transform(1, 0, 0, -1, round(x), round(h + y))
        # print(transform)
        # glif = svg2glif(svg_content, name, width=0, height=0, transform=transform)
        if name in font:
            glyph = font[name]
            glyph.clear()
        else:
            glyph = font.newGlyph(name)
        glyph.width, glyph.height = 0, 0
        glyph.unicode = None
        outline = SVGPath.fromstring(svg_content, transform=transform)
        point_pen = glyph.getPointPen()
        if rounding:
            segment_pen = SegmentToPointPen(RoundingPointPen(point_pen))
        else:
            segment_pen = SegmentToPointPen(point_pen)
        outline.draw(segment_pen)
        # break

        font.glyphOrder = [".notdef", "space"] + list(component_dict.keys())
    return

def write_features(font: ufoLib2.Font, fea_file=PATH_TO_FEA):
    with open(fea_file, "r") as f:
        features = f.read()
    font.features.text = features

def main():
    font = ufoLib2.Font()
    init(font)
    make_glyph_from_components(font)
    write_features(font)
    font.save(PATH_TO_UFO, overwrite=True)
    ttf = ufo2ft.compileTTF(
        font,
        removeOverlaps=True,      # 去除路径重叠
        reverseDirection=True,    # TTF 要求顺时针轮廓（CFF 是逆时针）
        convertCubics=True,       # 三次贝塞尔 → 二次（TTF glyf 表要求）
    )
    ttf.save(PATH_TO_TTF)


if __name__ == "__main__":
    main()