import re
from .grammar import Marker, ModifierPhrase, FingerPhrase, Note
from .constant import FINGER_LANG

def parse(s: str) -> Note:
  m = FINGER_LANG.search(s).groupdict()
  right_finger = m.get('right_finger')
  left_finger = m.get('left_finger')
  xian = parse_xian(m.get('xian'))
  hui = parse_hui(m.get('hui'))
  modifiers = parse_modifier(m.get('modifier'))
  marker = m.get('marker')

  return Note(
     rightor=FingerPhrase(finger=right_finger, numbers=xian),
     leftor=FingerPhrase(finger=left_finger, numbers=hui),
     modifiers=ModifierPhrase(modifiers),
     marker=Marker(marker),
  )

def parse_xian(s: str, p=re.compile(r'(一弦|二弦|三弦|四弦|五弦|六弦|七弦)')) -> list[str]:
  if s:
    return p.findall(s)

def parse_hui(s: str) -> list[str]:
  if not s:
    return
  if s == '徽外':
    return [s]
  else:
    index = s.index('徽')
    return [s[:index+1], s[index+1:]]

def parse_modifier(s: str, p=re.compile(r'(注|绰|吟|猱|上|下|急|缓|紧|慢)')) -> list[str]:
  if s:
    return p.findall(s)