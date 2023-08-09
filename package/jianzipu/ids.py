import re
from typing import Callable, Literal
class IDC:
  """表意文字描述符"""
  left_right='⿰'
  above_below='⿱'
  left_middle_right='⿲'
  above_middle_below='⿳'
  full_surround='⿴'
  surround_above='⿵'
  surround_below='⿶'
  surround_left='⿷'
  surround_upper_left='⿸'
  surround_upper_right='⿹'
  surround_lower_left='⿺'
  overlaid='⿻'

class IDS(str):
    pattern = re.compile(r'\[.*?\]')
    """表意文字描述序列"""
    def __init__(self, s:str) -> None:
        super().__init__()
        # if s is not in lambda form, we set it's operator form by default with an above-below structure
        if '〇' not in s:
            self.operator_form: Callable[[str], str] = lambda t: IDC.above_below + s + t
            self.operand_form = s
        # if s is in lambda form, we turns it in lambda expression
        else:
          self.operator_form: Callable[[str], str] = lambda t: s.replace('[','').replace(']','').replace('〇',t)
          self.operand_form = IDS.pattern.sub('', s).replace('〇','')

    def __add__(self, other):
        """addition as an another way to do above-below composition
        """
        assert isinstance(other, IDS), f"Don't support adding IDS with non-IDS"
        if str(self) == '':
            return other
        elif str(other) == '':
            return self
        return IDS(IDC.above_below + self.operand_form + other.operand_form)

    def __mul__(self, other):
        """multiplication as functional composition
        """
        assert isinstance(other, IDS), "Don't support multiplying IDS with non-IDS"
        if str(self) == '':
            return other
        elif str(other) == '':
            return self
        return IDS(self.operator_form(other.operand_form))

    def draw(self, by:Literal['zitool', 'native'] = 'zitool'):
        """draw the IDS
        """
        match by:
          case 'zitool':
              self._draw_by_zitool()
          case 'native':
              self._draw_by_native()
          case _:
              raise ValueError(f'Unsupported by={by}')

    def _draw_by_zitool(self, api=''):
        import requests
        from IPython import get_ipython
        from IPython.display import SVG, display
        api_json = "https://zi.tools/api/ids/lookupids/{}?replace_token"
        api_svg = "http://zu.zi.tools/{}.svg"
        response_json = requests.get(api_json.format(self))
        if response_json.status_code == 200:
            json = response_json.json()
            if json[self] is None:
                raise ValueError(f'Invalid IDS {self}')
        response_svg = requests.get(api_svg.format(self))
        if response_svg.status_code == 200:
            svg = response_svg.content
            if get_ipython():
                display(SVG(svg))
            else:
                with open('./zi.svg', 'w') as f:
                    f.write(svg)
                print('rendered svg saved to zi.svg')
        else:
            print('zitool server error')

    def _draw_by_native(self):
        raise NotImplementedError()