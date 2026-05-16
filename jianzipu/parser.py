from dataclasses import dataclass, field
from typing import List, Literal

from pyparsing import Group, Opt, ParserElement, ZeroOrMore, one_of

from .constants import (
  GLYPHS,
  CN_from_EN,
  EN_from_CN,
  t_JIANZI,
  t_TAG,
)

HUI_FINGER = sorted(GLYPHS.query("GlyphTag == 'hf'").GlyphNameCN.tolist(), key=len, reverse=True)
XIAN_FINGER = sorted(GLYPHS.query("GlyphTag == 'xf'").GlyphNameCN.tolist(), key=len, reverse=True)
MOVE_FINGER = sorted(GLYPHS.query("GlyphTag == 'mf'").GlyphNameCN.tolist(), key=len, reverse=True)
SPECIAL_FINGER = sorted(GLYPHS.query("GlyphTag == 'sf'").GlyphNameCN.tolist(), key=len, reverse=True)
MODIFIER = sorted(GLYPHS.query("GlyphTag == 'mo'").GlyphNameCN.tolist(), key=len, reverse=True)
JOINT_FINGER = sorted(GLYPHS.query("GlyphTag == 'jf'").GlyphNameCN.tolist(), key=len, reverse=True)
COMPLEX_FINGER = sorted(GLYPHS.query("GlyphTag == 'cf'").GlyphNameCN.tolist(), key=len, reverse=True)
MARKER = sorted(GLYPHS.query("GlyphTag == 'ma'").GlyphNameCN.tolist(), key=len, reverse=True)
XIAN_NUMBER_ORTHO = ['一弦','二弦','三弦','四弦','五弦','六弦','七弦']
HUI_NUMBER_ORTHO = ['十一徽','十二徽','十三徽','一徽','二徽','三徽','四徽','五徽','六徽','七徽','八徽','九徽','十徽']
FEN_NUMBER_ORTHO = ['一分','二分','三分','四分','五分','六分','七分','八分','九分','半']
HUI_FINGER_ORTHO = ['大指','食指','中指','名指','跪指','散音']
XIAN_NUMBER_ABBR = ['一','二','三','四','五','六','七']
HUI_NUMBER_ABBR = ['十一','十二','十三','一','二','三','四','五','六','七','八','九','十']
FEN_NUMBER_ABBR = ['一','二','三','四','五','六','七','八','九','半']

# white space is forbidden inside a note (but as a seperator between them)
ParserElement.set_default_whitespace_chars('')

class OrthoParseVar:
  # Define individual components
  hui_number = (ZeroOrMore((one_of(HUI_NUMBER_ORTHO) + Opt(one_of(FEN_NUMBER_ORTHO))) | '徽外')).set_results_name('hn')
  xian_number = (ZeroOrMore(one_of(XIAN_NUMBER_ORTHO))).set_results_name('xn')
  hui_finger = one_of(HUI_FINGER_ORTHO).set_results_name('hf')
  xian_finger = one_of(XIAN_FINGER).set_results_name('xf')
  move_finger = one_of(MOVE_FINGER).set_results_name('mf')
  special_finger = one_of(SPECIAL_FINGER).set_results_name('sf')
  modifier = one_of(MODIFIER).set_results_name('mo')
  complex_finger = one_of(COMPLEX_FINGER).set_results_name('cf')
  # TODO: should merge joint_finger and marker into one sTandalone Form called 'TF'
  joint_finger = one_of(JOINT_FINGER).set_results_name('jf')
  marker = one_of(MARKER).set_results_name('ma')

  # Define phrase patterns
  hui_finger_phrase = Group(hui_finger + hui_number).set_results_name('hfp')
  xian_finger_phrase = Group(xian_finger + xian_number).set_results_name('xfp')

  # reduced_xian_finger phrase, which is a simplified version of xian_finger_phrase
  # only used in complex form
  # since the complex_finger is actually the xian_finger 
  reduced_xian_finger_phrase = Group(xian_number).set_results_name('xfp')
  left_sub_phrase = Group(hui_finger_phrase + Opt(special_finger) + reduced_xian_finger_phrase).set_results_name('lsp')
  right_sub_phrase = Group(hui_finger_phrase + Opt(special_finger) + reduced_xian_finger_phrase).set_results_name('rsp')

  # move_finger_phrase is a similar to hui_finger_phrase, used in aside form
  move_finger_phrase = Group(move_finger + hui_number).set_results_name('mfp')


  # Define form pattern
  # simple form must have xian_finger_phrase, while hui_finger_phrase is optional
  simple_form = Group(Opt(hui_finger_phrase) + Opt(special_finger) + xian_finger_phrase).set_results_name('SF')
  # complex form must have all
  complex_form = Group(complex_finger + left_sub_phrase + right_sub_phrase).set_results_name('CF')
  # similar for aside_form
  aside_form = Group(Opt(modifier) + Opt(special_finger) + move_finger_phrase).set_results_name('AF')


  # 谱字, lazy matching, order is important
  PUZI = complex_form | marker | joint_finger | aside_form | simple_form

class AbbrParseVar:
  # Define individual components
  hui_number = (ZeroOrMore((one_of(HUI_NUMBER_ABBR) + Opt(one_of(FEN_NUMBER_ABBR))) | '外')).set_results_name('hn')
  xian_number = (ZeroOrMore(one_of(XIAN_NUMBER_ABBR))).set_results_name('xn')
  hui_finger = one_of(HUI_FINGER).set_results_name('hf')
  xian_finger = one_of(XIAN_FINGER).set_results_name('xf')
  move_finger = one_of(MOVE_FINGER).set_results_name('mf')
  special_finger = one_of(SPECIAL_FINGER).set_results_name('sf')
  modifier = one_of(MODIFIER).set_results_name('mo')
  complex_finger = one_of(COMPLEX_FINGER).set_results_name('cf')
  # TODO: should merge joint_finger and marker into one sTandalone Form called 'TF'
  joint_finger = one_of(JOINT_FINGER).set_results_name('jf')
  marker = one_of(MARKER).set_results_name('ma')

  # Define phrase patterns
  hui_finger_phrase = Group(hui_finger + hui_number).set_results_name('hfp')
  xian_finger_phrase = Group(xian_finger + xian_number).set_results_name('xfp')

  # reduced_xian_finger phrase, which is a simplified version of xian_finger_phrase
  # only used in complex from
  # since the complex_finger is actually the xian_finger 
  reduced_xian_finger_phrase = Group(xian_number).set_results_name('xfp')
  left_sub_phrase = Group(hui_finger_phrase + Opt(special_finger) + reduced_xian_finger_phrase).set_results_name('lsp')
  right_sub_phrase = Group(hui_finger_phrase + Opt(special_finger) + reduced_xian_finger_phrase).set_results_name('rsp')

  # move_finger_phrase is a similar to hui_finger_phrase, used in aside form
  move_finger_phrase = Group(move_finger + hui_number).set_results_name('mfp')


  # Define form pattern
  # simple form must have xian_finger_phrase, while hui_finger_phrase is optional
  simple_form = Group(Opt(hui_finger_phrase) + Opt(special_finger) + xian_finger_phrase).set_results_name('SF')
  # complex form must have all
  complex_form = Group(complex_finger + left_sub_phrase + right_sub_phrase).set_results_name('CF')
  # similar for aside_form
  aside_form = Group(Opt(modifier) + Opt(special_finger) + move_finger_phrase).set_results_name('AF')

  # 谱字, lazy matching, order is important
  PUZI = complex_form | marker | joint_finger | aside_form | simple_form


def parse(s: str, form : Literal['abbr','ortho'] = 'abbr'):
  match form:
    case 'abbr':
      d = AbbrParseVar.PUZI.parse_string(s).as_dict()
      # patch
      if 'CF' in d:
        # pop the mismatched number from hui_finger_phrase to xian_finger_phrase
        left_xian_number = d['CF']['lsp']['xfp']['xn']
        left_hui_number = d['CF']['lsp']['hfp']['hn']
        right_xian_number = d['CF']['rsp']['xfp']['xn']
        right_hui_number = d['CF']['rsp']['hfp']['hn']
        if len(left_xian_number) == 0:
          # case 1: mismatch e.g. ['十一'] instead of ['十'],['一']
          if (len(left_hui_number)) == 1 & (len(left_hui_number[0]) == 2):
            left_xian_number.append(left_hui_number[0][-1])
            left_hui_number[0] = left_hui_number[0][:-1]
          # case 2: mismatch e.g. ['十一','七'] instead of ['十一'],['七']
          else:
            left_xian_number.append(left_hui_number.pop(-1))
        if len(right_xian_number) == 0:
          # case 1: mismatch e.g. ['十一'] instead of ['十'],['一']
          if (len(right_hui_number)) == 1 & (len(right_hui_number[0])) == 2:
            right_xian_number.append(right_hui_number[0][-1])
            right_hui_number[0] = right_hui_number[0][:-1]
          # case 2: mismatch e.g. ['十一','七'] instead of ['十一'],['七']
          else:
            right_xian_number.append(right_hui_number.pop(-1))

    case 'ortho':
      d = OrthoParseVar.PUZI.parse_string(s).as_dict()

    case _:
      raise ValueError(f"form must be either 'abbr'or 'ortho'")
  # # debug
  # return d

  def remove_chars_from_dict(d, chars):
    if isinstance(d, dict):
        return {k: remove_chars_from_dict(v, chars) for k, v in d.items()}
    elif isinstance(d, list):
        return [remove_chars_from_dict(item, chars) for item in d]
    elif isinstance(d, str):
        return d.translate({ord(c): None for c in chars})
    else:
        return d

  d = remove_chars_from_dict(d, '徽分弦指音')

  return ParseNode.from_dict(d)

@dataclass
class ParseNode:
    tag: t_TAG
    name: t_JIANZI
    children: dict[t_JIANZI, "ParseNode"] = field(default_factory=dict)

    def __rich_repr__(self):
        yield "tag", self.tag
        if self.name:
            yield "name", self.name
        if self.children:
            yield "children", self.children

    def __post_init__(self) -> None:
        if self.name in CN_from_EN:
            self.name = CN_from_EN[self.name]

    @property
    def name_en(self) -> str:
        return EN_from_CN[self.name]

    def get_child(self, tag: t_TAG) -> "ParseNode":
        return self.children[tag]

    def get_children_tags(self):
        return tuple(self.children.keys())

    def is_leaf(self) -> bool:
        return not self.children

    def to_string(self, form: Literal['abbr', 'ortho'] = 'abbr') -> str:
        values: List[str] = []
    
        def traverse(node: "ParseNode") -> None:
            if node.is_leaf():
                tag = node.tag
                name = node.name
                if form == 'ortho':
                    if tag == 'hf':
                        if name in ['大', '食', '中', '名', '跪']:
                            name = name + '指'
                        elif name == '散':
                            name = '散音'
                    elif tag == 'hn1':
                        if name == '外':
                            name = '徽外'
                        elif name in HUI_NUMBER_ABBR:
                            name = name + '徽'
                    elif tag == 'hn2':
                        name = name + '分'
                    elif tag.startswith('xn'):
                        name = name + '弦'
                values.append(name)
            for child in node.children.values():
                traverse(child)

        traverse(self)
        return ''.join(values)

    def flatten(self) -> "ParseNode":
        """Return a new ParseNode with the same leaves but flattened structure."""
        leaves: list["ParseNode"] = []
        self._collect_leaves(leaves)
        return ParseNode(
            tag=self.tag,
            name=self.name,
            children={leaf.tag: leaf for leaf in leaves},
        )

    def _collect_leaves(self, leaves: list["ParseNode"]) -> None:
        if self.is_leaf():
            leaf = ParseNode(tag=self.tag, name=self.name)
            leaves.append(leaf)
            return
        for child in self.children.values():
            child._collect_leaves(leaves)

    @classmethod
    def from_dict(cls, d: dict) -> "ParseNode":
        assert len(d) == 1, "The dict should only have one key from 'SF', 'CF', 'AF', 'TF'"
        tag, content = next(iter(d.items()))
        return cls._build_node(tag, content)

    @classmethod
    def _build_node(cls, tag: t_TAG, content) -> "ParseNode":
        if isinstance(content, str):
            return cls(tag=tag, name=content)
        if isinstance(content, dict):
            node = cls(tag=tag, name='')
            for key, val in content.items():
                if isinstance(val, list):
                    for i, item in enumerate(val, start=1):
                        child = cls(
                            tag=f"{key}{i}",
                            name=item
                        )
                        node.children[child.tag] = child
                else:
                        node.children[key] = cls._build_node(key, val)
            return node
        raise TypeError(f"Unsupported node content type: {type(content)}")