from pathlib import Path
from types import SimpleNamespace

from fontTools.misc.transform import Transform
from fontTools.pens.pointPen import SegmentToPointPen
from fontTools.pens.roundingPen import RoundingPointPen
from fontTools.svgLib import SVGPath
from fontTools.ufoLib.glifLib import writeGlyphToString

from .constants import PATH_TO_FONT, PATH_TO_SVGS
from .layout import parse_figma
from .metadata import METADATA

PATH_TO_UFO = PATH_TO_FONT / Path(METADATA.fontname).with_suffix('.ufo')
PATH_TO_TTF = PATH_TO_FONT / Path(METADATA.fontname).with_suffix('.ttf')

def svg2glif(svg, name, width=0, height=0, unicodes=None, transform=None, version=2, rounding=True):
    """Convert an SVG outline to a UFO glyph with given 'name', advance
    'width' and 'height' (int), and 'unicodes' (list of int).
    Return the resulting string in GLIF format (default: version 2).
    If 'transform' is provided, apply a transformation matrix before the
    conversion (must be tuple of 6 floats, or a FontTools Transform object).
    """
    glyph = SimpleNamespace(width=width, height=height, unicodes=unicodes)
    outline = SVGPath.fromstring(svg, transform=transform)

    # writeGlyphToString takes a callable (usually a glyph's drawPoints
    # method) that accepts a PointPen, however SVGPath currently only has
    # a draw method that accepts a segment pen. We need to wrap the call
    # with a converter pen.
    def drawPoints(pointPen):
        if rounding:
            pen = SegmentToPointPen(RoundingPointPen(pointPen))
        else:
            pen = SegmentToPointPen(pointPen)
        outline.draw(pen)

    return writeGlyphToString(
        name, glyphObject=glyph, drawPointsFunc=drawPoints, formatVersion=version
    ) 

def make_glyph_from_components(ufo_dir: Path):
    _, _, component_dict = parse_figma()
    for name, component in component_dict.items():
        svg_path = PATH_TO_SVGS / f"c_{name}.svg"
        with open(svg_path, "r", encoding="utf-8") as f:
            svg_content = f.read()
        x, y, w, h = component.xywh
        # transform from svg coordinate system (y down) to font coordinate system (y up)
        transform = Transform(1, 0, 0, -1, round(x), round(h + y))
        print(transform)
        glif = svg2glif(svg_content, name, width=0, height=0, transform=transform)
        glyph_path = ufo_dir / "glyphs" / f"{name}.glif"
        glyph_path.parent.mkdir(parents=True, exist_ok=True)
        with open(glyph_path, "w", encoding="utf-8") as f:
            f.write(glif)
        break
    return

def main():
    PATH_TO_UFO.mkdir(exist_ok=True, parents=True)
    make_glyph_from_components(PATH_TO_UFO)

if __name__ == "__main__":
    main()