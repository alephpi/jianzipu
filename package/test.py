from jianzipu.jianzipu.parser import parse, transcribe

def test_simple_form_parse_and_str():
  l = [
      '大指一徽六分勾三弦',
      '大指二徽剔四弦',
      '跪指三徽七分抹五弦',
      '跪指四徽挑六弦',
      '名指五徽八分注托七弦',
      '名指六徽注擘一弦',
      '中指七徽打二弦',
      '中指八徽九分摘三弦',
      '食指十徽绰打四弦',
      '食指徽外绰打五弦',
      '中指徽外摘六弦',
      '中指徽外历二弦三弦',
      '散音历二弦三弦',
      '大指七徽六分掩',
      '名指七徽六分搯起',
      # '打圆',
      # '不动',
      # '推出',
      # '滚拂',
      ]
  for i in l:
    assert str(parse(i, form='ortho')) == i

def test_abbr_simple_form_parse_and_str():
  l = [
      '大一六勾三',
      '大二剔四',
      '跪三七抹五',
      '跪四挑六',
      '名五八注托七',
      '名六注擘一',
      '中七打二',
      '中八九摘三',
      '食十绰打四',
      '食外绰打五',
      '中外摘六',
      '中外历二三',
      '散历二三',
      '大七六掩',
      '名七六搯起',
      '名十二搯起',
      '名十二三搯起',
      # '打圆',
      # '不动',
      # '推出',
      # '滚拂',
      ]

  for i in l:
    assert str(parse(i, form='abbr')) == i

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
    assert str(parse(i, form='ortho')) == i

def test_abbr_complex_form_parse_and_str():
  l = [
      '撮大七七散六',
      '撮大七七名六二五',
      '撮大五六名六二五',
      '撮大三六四散五',
      '撮大五七散六',
      '撮大外七散六',
      ]
  for i in l:
    assert str(parse(i, form='abbr')) == i

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
    assert str(parse(i, form='ortho')) == i

def test_abbr_aside_form_parse_and_str():
  l = [
      '上七六',
      '下五四',
      '进',
      '退',
      '进复',
      '退复',
      '慢上七六',
      '紧下五四',
      '引上七六',
      '淌下五四',
      '注上七六',
      '绰下五四',
      '注吟',
      '绰猱',
      '急撞',
      ]
  for i in l:
    assert str(parse(i, form='abbr')) == i

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
    assert str(parse(i, form='ortho')) == i


def test_transcribe():

  abbr = [
      '大一六勾三',
      '大二剔四',
      '跪三七抹五',
      '跪四挑六',
      '名五八注托七',
      '名六注擘一',
      '中七打二',
      '中八九摘三',
      '食十绰打四',
      '食外绰打五',
      '中外摘六',
      '中外历二三',
      '散历二三',
      '大七六掩',
      '名七六搯起',
      '打圆',
      '不动',
      '推出',
      '滚拂',
      ]

  ortho = [
      '大指一徽六分勾三弦',
      '大指二徽剔四弦',
      '跪指三徽七分抹五弦',
      '跪指四徽挑六弦',
      '名指五徽八分注托七弦',
      '名指六徽注擘一弦',
      '中指七徽打二弦',
      '中指八徽九分摘三弦',
      '食指十徽绰打四弦',
      '食指徽外绰打五弦',
      '中指徽外摘六弦',
      '中指徽外历二弦三弦',
      '散音历二弦三弦',
      '大指七徽六分掩',
      '名指七徽六分搯起',
      '打圆',
      '不动',
      '推出',
      '滚拂',
      ]

  for i, j in zip(abbr, ortho):
    assert str(transcribe(i)) == j

def test_char():
  pass

def test_parse_error():
  pass
