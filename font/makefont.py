import json

import fontforge
from constant import *

import font


def load_data():
    with open(NUMBER_DATA_PATH, "r", encoding="utf-8") as f:
        number_components = json.load(f)
        number_components = [font.Component.model_validate(comp) for comp in number_components]
    with open(HUI_FINGER_DATA_PATH, "r", encoding="utf-8") as f:
        hui_finger_components = json.load(f)
        hui_finger_components = [font.Component.model_validate(comp) for comp in hui_finger_components]
    with open(XIAN_FINGER_DATA_PATH, "r", encoding="utf-8") as f:
        xian_finger_layouts = json.load(f)
        xian_finger_layouts = [font.Frame.model_validate(comp) for comp in xian_finger_layouts]

    return number_components, hui_finger_components, xian_finger_layouts

def make_glyph(font: fontforge.font, components: list[font.Component]):
    """
    将Layout及其components转换为FontForge字形
    
    Args:
        font_path: 字体文件路径
        layout: Layout对象，包含组件信息
        glyph_name: 目标字形名称
    """
    if not components:
        print("components is empty")
        return
    glyph_name = "_".join([comp.name for comp in components])
    glyph = font.createChar(-1, glyph_name)
    glyph.clear()  # 清除现有内容
    
    # 设置字形宽度
    glyph.width = int(GLYPH_WIDTH)
    
    # 导入第一个组件到前景层
    first_comp = components[0]
    glyph.importOutlines(first_comp.svg_path, scale=False)
    
    # 应用第一个组件的位置
    glyph.transform((1, 0, 0, 1, first_comp.absolute.x, first_comp.absolute.y))
    
    # 导入其余组件
    for i, comp in enumerate(components[1:], start=1):
        # 创建新层
        layer = fontforge.layer()
        # 导入SVG到新层
        glyph.importOutlines(comp.svg_path, scale=False)
        # newly imported contour is appended to foreground layer
        contour = glyph.foreground[i]
        # 应用位置偏移
        contour.transform((1, 0, 0, 1, comp.absolute.x, comp.absolute.y))
    
    # 优化字形
    # glyph.removeOverlap()
    # glyph.addExtrema()
    # glyph.simplify()
    # glyph.round()
    
    # 确保字形在正确的边界内
    # glyph.left_side_bearing = 0
    # glyph.right_side_bearing = GLYPH_WIDTH - (glyph.bounds[2] - glyph.bounds[0])

def generate_xian_finger_number_ligature(xian_finger_layouts: list[font.Frame], number_components: list[font.Component]):
    ...