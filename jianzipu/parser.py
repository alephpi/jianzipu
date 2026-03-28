from dataclasses import dataclass, field
from typing import List, Literal

from pyparsing import Group, Opt, ParserElement, ZeroOrMore, one_of

from .constant import d

# fingers, modifiers and markers are open, so we import from outside
# 保证字符长的在前（如防止勾剔只匹配了勾）
HUI_FINGER = sorted(d['徽位指法'].keys(), key=len, reverse=True)
XIAN_FINGER = sorted(d['弦序指法'].keys(), key=len, reverse=True)
MOVE_FINGER = sorted(d['走位指法'].keys(), key=len, reverse=True)
SPECIAL_FINGER = sorted(d['特殊指法'].keys(), key=len, reverse=True)
MODIFIER = sorted(d['修饰'].keys(), key=len, reverse=True)
BOTH_FINGER = sorted(d['联袂指法'].keys(), key=len, reverse=True)
COMPLEX_FINGER = sorted(d['复式指法'].keys(), key=len, reverse=True)
MARKER = sorted(d['记号'].keys(), key=len, reverse=True)

# white space is forbidden inside a note (but as a seperator between them)
ParserElement.set_default_whitespace_chars('')

class OrthoParseVar:
  # numbers are closed, so we list here
  XIAN = ['一弦','二弦','三弦','四弦','五弦','六弦','七弦']
  HUI = ['十一徽','十二徽','十三徽','一徽','二徽','三徽','四徽','五徽','六徽','七徽','八徽','九徽','十徽']
  FEN = ['一分','二分','三分','四分','五分','六分','七分','八分','九分','半']
  # Define individual components
  hui = (ZeroOrMore((one_of(HUI) + Opt(one_of(FEN))) | '徽外')).set_results_name('hn')
  xian = (ZeroOrMore(one_of(XIAN))).set_results_name('xn')
  hui_finger = one_of(HUI_FINGER).set_results_name('hf')
  xian_finger = one_of(XIAN_FINGER).set_results_name('xf')
  move_finger = one_of(MOVE_FINGER).set_results_name('mf')
  special_finger = one_of(SPECIAL_FINGER).set_results_name('sf')
  modifier = one_of(MODIFIER).set_results_name('mod')
  complex_finger = one_of(COMPLEX_FINGER).set_results_name('cf')
  both_finger = one_of(BOTH_FINGER).set_results_name('bf')
  marker = one_of(MARKER).set_results_name('marker')

  # Define phrase patterns
  hui_finger_phrase = Group(hui_finger + hui).set_results_name('hfp')
  xian_finger_phrase = Group(xian_finger + xian).set_results_name('xfp')

  # reduced_xian_finger phrase, which is a simplified version of xian_finger_phrase
  # only used in complex form
  # since the complex_finger is actually the xian_finger 
  reduced_xian_finger_phrase = Group(xian).set_results_name('xfp')
  left_sub_phrase = Group(hui_finger_phrase + Opt(special_finger) + reduced_xian_finger_phrase).set_results_name('lsp')
  right_sub_phrase = Group(hui_finger_phrase + Opt(special_finger) + reduced_xian_finger_phrase).set_results_name('rsp')

  # move_finger_phrase is a similar to hui_finger_phrase, used in aside form
  move_finger_phrase = Group(move_finger + hui).set_results_name('mfp')


  # Define form pattern
  # simple form must have xian_finger_phrase, while hui_finger_phrase is optional
  simple_form = Group(Opt(hui_finger_phrase) + Opt(special_finger) + xian_finger_phrase).set_results_name('SF')
  # complex form must have all
  complex_form = Group(complex_finger + left_sub_phrase + right_sub_phrase).set_results_name('CF')
  # similar for aside_form
  aside_form = Group(Opt(modifier) + Opt(special_finger) + move_finger_phrase).set_results_name('AF')

  # 谱字, lazy matching, order is important
  PUZI = complex_form | marker | both_finger | aside_form | simple_form

class AbbrParseVar:
  # numbers are closed, so we list here
  XIAN = ['一','二','三','四','五','六','七']
  HUI = ['十一','十二','十三','一','二','三','四','五','六','七','八','九','十']
  FEN = ['一','二','三','四','五','六','七','八','九','半']
  HUI_FINGER = ['大','食','中','名','跪','散']
  # Define individual components
  hui = (ZeroOrMore((one_of(HUI) + Opt(one_of(FEN))) | '外')).set_results_name('hn')
  xian = (ZeroOrMore(one_of(XIAN))).set_results_name('xn')
  hui_finger = one_of(HUI_FINGER).set_results_name('hf')
  xian_finger = one_of(XIAN_FINGER).set_results_name('xf')
  move_finger = one_of(MOVE_FINGER).set_results_name('mf')
  special_finger = one_of(SPECIAL_FINGER).set_results_name('sf')
  modifier = one_of(MODIFIER).set_results_name('mod')
  complex_finger = one_of(COMPLEX_FINGER).set_results_name('cf')
  # TODO: should merge both_finger and marker into one sTandalone Form called 'TF'
  both_finger = one_of(BOTH_FINGER).set_results_name('bf')
  marker = one_of(MARKER).set_results_name('marker')

  # Define phrase patterns
  hui_finger_phrase = Group(hui_finger + hui).set_results_name('hfp')
  xian_finger_phrase = Group(xian_finger + xian).set_results_name('xfp')

  # reduced_xian_finger phrase, which is a simplified version of xian_finger_phrase
  # only used in complex from
  # since the complex_finger is actually the xian_finger 
  reduced_xian_finger_phrase = Group(xian).set_results_name('xfp')
  left_sub_phrase = Group(hui_finger_phrase + Opt(special_finger) + reduced_xian_finger_phrase).set_results_name('lsp')
  right_sub_phrase = Group(hui_finger_phrase + Opt(special_finger) + reduced_xian_finger_phrase).set_results_name('rsp')

  # move_finger_phrase is a similar to hui_finger_phrase, used in aside form
  move_finger_phrase = Group(move_finger + hui).set_results_name('mfp')


  # Define form pattern
  # simple form must have xian_finger_phrase, while hui_finger_phrase is optional
  simple_form = Group(Opt(hui_finger_phrase) + Opt(special_finger) + xian_finger_phrase).set_results_name('SF')
  # complex form must have all
  complex_form = Group(complex_finger + left_sub_phrase + right_sub_phrase).set_results_name('CF')
  # similar for aside_form
  aside_form = Group(Opt(modifier) + Opt(special_finger) + move_finger_phrase).set_results_name('AF')

  # 谱字, lazy matching, order is important
  PUZI = complex_form | marker | both_finger | aside_form | simple_form


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
    label: str
    value: str
    children: List["ParseNode"] = field(default_factory=list)

    def is_leaf(self) -> bool:
        return not self.children

    def to_string(self, form: Literal['abbr', 'ortho'] = 'abbr') -> str:
        values: List[str] = []
    
        def traverse(node: "ParseNode") -> None:
            if node.is_leaf():
                label = node.label
                value = node.value
                if form == 'ortho':
                    if label == 'hf':
                        if value in ['大', '食', '中', '名', '跪']:
                            value = value + '指'
                        elif value == '散':
                            value = '散音'
                    elif label == 'hn1':
                        if value == '外':
                            value = '徽外'
                        elif value in ['一', '二', '三', '四', '五', '六', '七', '八', '九', '十', '十一', '十二', '十三']:
                            value = value + '徽'
                    elif label == 'hn2':
                        value = value + '分'
                    elif label.startswith('xn'):
                        value = value + '弦'
                values.append(value)
            for child in node.children:
                traverse(child)
    
        traverse(self)
        return ''.join(values)

    @classmethod
    def from_dict(cls, d: dict) -> "ParseNode":
        assert len(d) == 1, "The dict should only have one key from 'SF', 'CF', 'AF', 'TF'"
        label, content = next(iter(d.items()))
        return cls._build_node(label, content)

    @classmethod
    def _build_node(cls, label: str, content) -> "ParseNode":
        if isinstance(content, str):
            return cls(label=label, value=content)
        if isinstance(content, dict):
            node = cls(label=label, value='')
            for key, val in content.items():
                if isinstance(val, list):
                    for i, item in enumerate(val, start=1):
                        child = cls(
                            label=f"{key}{i}",
                            value=item
                        )
                        node.children.append(child)
                else:
                    node.children.append(cls._build_node(key, val))
            return node
        raise TypeError(f"Unsupported node content type: {type(content)}")