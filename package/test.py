from jianzipu.jianzipu.parser import parse

def test_simple_form_parse_and_str():
  l = [
      '大指七徽六分勾三弦',
      '跪指五徽八分挑六弦',
      '名指一徽九分注挑二弦',
      '食指十二徽半绰抹挑四弦',
      '中指徽外勾剔七弦',
      '中指徽外历二弦三弦',
      '散音历二弦三弦',
      '大指七徽六分掩',
      '名指七徽六分掐起',
      '打圆',
      '不动',
      '推出',
      '滚拂',
      ]
  for i in l:
    assert str(parse(i)) == i

def test_complex_form_parse_and_str():
  l = [
      '撮大指七徽七弦散音六弦',
      '撮大指七徽七弦名指六徽二分五弦',
      '撮大指五徽六分名指六徽二分五弦',
      '撮大指三徽六分四弦散音五弦',
      '撮大指八徽五分七弦散音六弦',
      '撮大指徽外七弦散音六弦',
      ]
  for i in l:
    assert str(parse(i)) == i

def test_aside_form_parse_and_str():
  l = [
      '上七徽六分',
      '下五徽四分',
      '进',
      '退',
      '进复',
      '退复',
      '慢上七徽六分',
      '紧下五徽四分',
      '引上七徽六分',
      '淌下五徽四分',
      '注上七徽六分',
      '绰下五徽四分',
      '注吟',
      '绰猱',
      '急撞',
      ]
  for i in l:
    assert str(parse(i)) == i

def test_marker_form_parse_and_str():
  l = [
      '少息',
      '大息',
      '入拍',
      '入慢',
      '。',
      '再作',
      '从头再作',
      '曲终',
      '操终',
      ]
  for i in l:
    assert str(parse(i)) == i

def test_char():
  pass

def test_parse_error():
  pass
