class Symbol():
    def __init__(self) -> None:
        self.name = None # 减字符号名称
        self.valence = 0 # 价位，指法字配合的弦位字个数。譬如勾的价位为1，历的价位为2或3

class Leftor(Symbol):
    domain = ['散音',
              '大指','食指','中指','名指','上','下','就','绰','注','吟','猱',
              #'进','退','复进','复退','复','引上','淌下','往来','撞','掐起','带起',
              #'罨','推出','不动',
              ]
    domain.sort(key=lambda x: len(x), reverse=True)
    pattern = '|'.join(domain)

class Rightor(Symbol):
    domain = ['擘','托','抹','挑','勾','剔','打','摘','抹挑','勾剔',
              #'历','蠲','轮','琐','长琐',
              #'如一声','双弹','拨','剌','拨剌','伏','撮','打圆','滚','拂','滚拂','全扶'
              ]
    domain.sort(key=lambda x: len(x), reverse=True)
    pattern = '|'.join(domain)

class Bothor(Symbol):
    domain = ['分开','同声','应合','放合','掐撮声','掐撮三声']
    domain.sort(key=lambda x: len(x), reverse=True)
    pattern = '|'.join(domain)

class Marker(Symbol):
    domain = ['泛起','泛止', # 泛音、按音符号不单独出现注明，散音视为一种特殊的左手指法（即无指法），省略之
              '少息','大息','急','缓','紧','曼','入拍','入慢','。','间','再作','从头再作','曲终','操终']
    domain.sort(key=lambda x: len(x), reverse=True)
    pattern = '|'.join(domain)

class Xian(Symbol):
    domain = ['一弦','二弦','三弦','四弦','五弦','六弦','七弦']
    domain.sort(key=lambda x: len(x), reverse=True)
    pattern = '|'.join(domain)

class Hui(Symbol):
    domain = ['一徽','二徽','三徽','四徽','五徽','六徽','七徽','八徽','九徽','十徽','十一徽','十二徽','十三徽']
    domain.sort(key=lambda x: len(x), reverse=True)
    pattern = '|'.join(domain)

class Fen(Symbol):
    domain = ['一分','二分','三分','四分','五分','六分','七分','八分','九分']
    domain.sort(key=lambda x: len(x), reverse=True)
    pattern = '|'.join(domain)