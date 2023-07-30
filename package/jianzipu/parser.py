import re
from typing import Dict
from .symbol import Leftor, Rightor, Bothor, Marker, Xian, Hui, Fen

def parse(s: str) -> Dict:
  """减字谱解析器

  Args:
      s (str):用自然语言描述的谱，也就是减字谱的读法
  """
  rightor = None
  leftor = None
  xian = None
  hui = None
  fen = None
  modifiers = None

  # 右手
  group = re.match(Rightor.pattern,s)
  if group is not None:
    rightor = group[0]
    _, post = s.split(rightor)
    # 弦位
    group = re.match(Xian.pattern, post)
    if group is not None:
      xian = group[0] 
    else:
      raise ValueError(f'弦位“{post}”有误')

  # 左手
  group = re.match(Leftor.pattern, s)
  if group is not None:
    leftor = group[0]
    pre, post = s.split(leftor)
    # 左手后为徽位
    group = re.match(Hui.pattern, post)
    if group is not None:
      hui = group[0]
      _, post = post.split(hui)
      # 徽位后为分位
      group = re.match(Fen.pattern, post)
      if group is not None:
        fen = group[0]
    else:
      raise ValueError(f'徽位“{post}”有误')

  return {
    'rightor': rightor,
    'leftor': leftor,
    'xian': xian,
    'hui': hui,
    'fen': fen,
    'modifiers': modifiers,
    }

  