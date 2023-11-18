from typing import Literal
import numpy as np

from package.jianzipu.jianzipu.grammar import AsideForm, ComplexForm, Note, NumberPhrase, SimpleForm
# 泛音徽位 = [1/8, 1/6, 1/5, 1/4, 1/3, 2/5, 1/2, 3/5, 2/3, 3/4, 4/5, 5/6, 7/8, 1]
# 对应徽位发出泛音为基频的倍数
泛音徽位 = [8, 6, 5, 4, 3, 5, 2, 5, 3, 4, 5, 6, 8]
# def hui_to_ratio(hui: int, fen: int = 0):
#     ratio = HUI[hui-1] + (HUI[hui] - HUI[hui-1]) * fen / 10
#     return round(ratio,4)

# 岳山到徽位的距离占总弦长之分数
按音徽位 = np.array([
  0.125, 0.1292, 0.1333, 0.1375, 0.1417, 0.1458, 0.15, 0.1542, 0.1583, 0.1625, 
  0.1667, 0.17, 0.1733, 0.1767, 0.18, 0.1833, 0.1867, 0.19, 0.1933, 0.1967, 
  0.2, 0.205, 0.21, 0.215, 0.22, 0.225, 0.23, 0.235, 0.24, 0.245, 
  0.25, 0.2583, 0.2667, 0.275, 0.2833, 0.2917, 0.3, 0.3083, 0.3167, 0.325, 
  0.3333, 0.34, 0.3467, 0.3533, 0.36, 0.3667, 0.3733, 0.38, 0.3867, 0.3933, 
  0.4, 0.41, 0.42, 0.43, 0.44, 0.45, 0.46, 0.47, 0.48, 0.49, 
  0.5, 0.51, 0.52, 0.53, 0.54, 0.55, 0.56, 0.57, 0.58, 0.59, 
  0.6, 0.6067, 0.6133, 0.62, 0.6267, 0.6333, 0.64, 0.6467, 0.6533, 0.66, 
  0.6667, 0.675, 0.6833, 0.6917, 0.7, 0.7083, 0.7167, 0.725, 0.7333, 0.7417, 
  0.75, 0.755, 0.76, 0.765, 0.77, 0.775, 0.78, 0.785, 0.79, 0.795, 
  0.8, 0.8033, 0.8067, 0.81, 0.8133, 0.8167, 0.82, 0.8233, 0.8267, 0.83, 
  0.8333, 0.8375, 0.8417, 0.8458, 0.85, 0.8542, 0.8583, 0.8625, 0.8667, 0.8708, 
  0.875, 0.8875, 0.9, 0.9125, 0.925, 0.9375, 0.95, 0.9625, 0.975, 0.9875
])


def hui_to_ratio(hui:int, fen:int = 0, overtone=False):
    if overtone:
      return 泛音徽位[hui-1]
    else:
      return 1/按音徽位[(hui-1)*10 + fen]



def ratio_to_hui(ratio: float):
    idx = np.argmin(np.abs(按音徽位 - ratio))
    return idx // 10 + 1, idx % 10


# 十二律 = {
#   '黄钟': 1.000000000000000000000000,
#   '应锺': 1.059463094359295264561825,
#   '无射': 1.122462048309372981433533,
#   '南吕': 1.189207115002721066717500,
#   '夷则': 1.259921049894873164767211,
#   '林锺': 1.334839854170034364830832,
#   '蕤宾': 1.414213562373095048801689,
#   '仲吕': 1.498307076876681498799281,
#   '姑洗': 1.587401051968199474751706,
#   '夹锺': 1.681792830507429086062251,
#   '太蔟': 1.781797436280678609480452,
#   '大吕': 1.887748625363386993283826,
# }

# 各音到宫的相对距离
# 五音 = {
#     '宫': 0,
#     '商': 2,
#     '角': 4,
#     '徵': 7,
#     '羽': 9,
#     }

MODES = {
    '正调': [-5, -3, 0, 2, 4, 7, 9],
}

NUMBER = {
 '一': 1,
 '二': 2,
 '三': 3,
 '四': 4,
 '五': 5,
 '六': 6,
 '七': 7,
 '八': 8,
 '九': 9,
 '十': 10,
 '十一':11,
 '十二':12,
 '十三':13,
 '外':14,
 '半': 5
}

def parse_number(n: NumberPhrase):
    n = (NUMBER[i.id] for i in n)
    return n

class Qin:
    def __init__(self, tonic: float, mode: str, timbre = None):
        """
        Args:
            tonic (float): 宫音频率
            mode (_type_): 调式，即调式对应的弦法
            timbre (_type_, optional): 音色，须是一个波形
        """
        #宫音频率
        self.tonic = tonic
        #调式，即调式对应的弦法
        assert mode in MODES, f"{mode} is not in {MODES}"
        config = MODES[mode]
        self.mode = [self.tonic * 2**(i/12) for i in config]

        #音色，须是一个波形
        self.timbre = timbre

        #状态，减字谱是依赖上文的
        self._F0 = 0
        self._overtone = False
        self._hui = None
    
    def _update_state(self, note):
      raise NotImplementedError

    def _play_xian_on_hui(self, xian: int, hui: tuple[int, int], overtone: bool):
        self.F0 =  self.mode[xian-1] * hui_to_ratio(hui=hui[0], fen=hui[1], overtone=overtone)
        raise NotImplementedError

    def play(self, note: Note, duration=1):
        # 产生一个波形，以指法确定基频，音色确定包络
        if isinstance(note, SimpleForm):
            xian = parse_number(note.xian_finger_phrase.number)
            hui = parse_number(note.hui_finger_phrase.number)
            for xi in xian:
                self._play_xian_on_hui(xi, hui)
        elif isinstance(note, ComplexForm):
            pass
        elif isinstance(note, AsideForm):
            pass
        else:
            raise ValueError(f"{note} is not a valid form")
        self._update_state(note)


        pass