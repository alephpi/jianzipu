import re
from .note import Note
from .symbol import Finger, Modifier, Marker, Number, Phrase

# 保证匹配字符长的在前（防止勾剔只匹配了勾）
LEFT_FINGER = re.compile(r'(散音|大指|食指|中指|名指|跪指)')
RIGHT_FINGER = re.compile(r'(抹挑|勾剔|擘|托|抹|挑|勾|剔|打|摘|历)')
BOTH_FINGER = re.compile(r'(掐撮三声|掐撮声|分开|同声|应合|放合)')
MODIFIER = re.compile(r'(注|绰|吟|猱|上|下|急|缓|紧|慢)')
MARKER = re.compile(r'(从头再作|泛起|泛止|少息|大息|入拍|入慢|再作|曲终|操终|。|间)')
XIAN = re.compile(r'(一弦|二弦|三弦|四弦|五弦|六弦|七弦)')
HUI = re.compile(r'((十一徽|十二徽|十三徽|一徽|二徽|三徽|四徽|五徽|六徽|七徽|八徽|九徽|十徽)(一分|二分|三分|四分|五分|六分|七分|八分|九分|半)?|徽外)')
NUMBERS = {'一':1,'二':2,'三':3,'四':4,'五':5,'六':6,'七':7,'八':8,'九':9,'十':10,'十一':11,'十二':12,'十三':13,'半':5}

def parse(s: str) -> Note:
  """减字谱解析器

  Args:
      s (str):用自然语言描述的谱，也就是减字谱的读法
  """
  rightor = parse_rightor(s)
  leftor = parse_leftor(s)
  bothor = parse_bothor(s)
  modifiers = parse_modifier(s) 
  marker = parse_marker(s) 

  return Note(rightor, leftor, bothor, modifiers, marker)

def parse_rightor(s: str) -> Phrase:
  r = RIGHT_FINGER.findall(s)[0]
  x = XIAN.findall(s)
  right = Finger(r)
  xian = [Number(n, parse_number(n)) for n in x]
  return Phrase(right, xian)

def parse_leftor(s: str) -> Phrase:
  l = LEFT_FINGER.findall(s)[0]
  h = HUI.findall(s)
  left = Finger(l)
  hui = [Number(n[0], parse_number(n[0])) for n in h]
  return Phrase(left, hui)

def parse_bothor(s: str) -> Phrase:
   return

def parse_number(s: str) -> Number:
  if '弦' in s:
      number = NUMBERS[s.strip('弦')]
  elif '徽' in s:
      if s == '徽外':
          number = 14
      else:
          i,d = s.replace('徽',',').replace('分','').split(',')
          number = NUMBERS[i] + 0.1 * NUMBERS.get(d, 0)
  else:
     print(s, 'something went wrong')
  return number

def parse_modifier(s: str) -> Modifier:
  m = MODIFIER.findall(s)
  modifiers = [Modifier(n) for n in m]
  return modifiers

def parse_marker(s: str) -> Marker:
  m = MARKER.findall(s)
  marker = [Marker(n) for n in m]
  return marker