% abbr: 
% hp, xp, np: HuiPhrase, XianPhrase, NumberPhrase
% axp, rxp: annotatedXianPhrase, reducedXianPhrase
% hf, xf, sf: HuiFinger, XianFinger, SpecialFinger
% n: number

% constants
:- dynamic(l_HUI_FINGER/1).
:- dynamic(l_XIAN_FINGER/1).
:- dynamic(l_MOVE_FINGER/1).
:- dynamic(l_SPECIAL_FINGER/1).
:- dynamic(l_BOTH_FINGER/1). 
:- dynamic(l_COMPLEX_FINGER/1). 
:- dynamic(l_MODIFIER/1).
:- dynamic(l_MARKER/1).


l_XIAN(['一弦','二弦','三弦','四弦','五弦','六弦','七弦','一','二','三','四','五','六','七']).
l_HUI(['十一徽','十二徽','十三徽','一徽','二徽','三徽','四徽','五徽','六徽','七徽','八徽','九徽','十徽','徽外','十一','十二','十三','一','二','三','四','五','六','七','八','九','十','外']).
l_FEN(['一分','二分','三分','四分','五分','六分','七分','八分','九分','半','一','二','三','四','五','六','七','八','九']).

l_HUI_FINGER(['散音', '大指', '食指', '中指', '名指', '跪指', '散', '大', '食', '中', '名', '跪']).
l_XIAN_FINGER(['如一声', '抹挑', '勾剔', '打摘', '托擘', '半轮', '长琐', '如一', '滚拂', '全扶', '剌伏', '打圆', '搯起', '抓起', '带起', '虚掩', '推出', '不动', '擘', '托', '抹', '挑', '勾', '剔', '打', '摘', '历', '蠲', '轮', '琐', '伏', '滚', '拂', '至', '拨', '剌', '掩']).
l_MOVE_FINGER(['进复', '退复', '往来', '上', '下', '进', '退', '复', '撞', '逗', '唤', '吟', '猱']).
l_SPECIAL_FINGER(['注', '绰']).
l_BOTH_FINGER(['掐撮三声', '分开', '同声', '应合', '放合']).
l_COMPLEX_FINGER(['掐撮', '双弹', '拨剌', '齐撮', '撮']).
l_MODIFIER(['引', '淌', '急', '缓', '紧', '慢']).
l_MARKER(['从「再作', '从头再作', '少息', '大息', '入拍', '入慢', '句号', '再作', '曲终', '操终', '泛起', '泛止', '。', '间', '「']).

% helper function
in(X, List) :- call(List,L), member(X, L).

parser([]) --> [].
parser(Tree) --> complex(Tree).
parser(Tree) --> marker(Tree).
parser(Tree) --> bf(Tree).
parser(Tree) --> aside(Tree).
parser(Tree) --> simple(Tree).

% form
simple(simple_form(HP, SF, XP)) --> hp(HP), sf(SF), xp(XP).
complex(complex_form(CF,left_sub_phrase(LSP), right_sub_phrase(RSP))) --> cf(CF), sp(LSP), sp(RSP).
aside(aside_form(M,SF,MF)) --> modifier(M), sf(SF), mf(MF).



% finger_phrase
hp(hui_finger_phrase(HF, NP)) --> hf(HF), hnp(NP).
xp(xian_finger_phrase(XF, NP)) --> xf(XF), xnp(NP).
% trealla-prolog is different from swi-prolog, it doesn't support `pred()` syntax
% here we have to put a placeholder null for the functor. 
rxp(xian_finger_phrase(finger({null}), number(N))) --> [N],{in(N, l_XIAN)}.

sp((HP, SF, RXP)) --> hp(HP), sf(SF), rxp(RXP).


% atoms

%% finger is an atom
hf(finger({null})) --> [].
hf(finger(F)) --> [F], { in(F, l_HUI_FINGER) }.
xf(finger({null})) --> [].
xf(finger(F)) --> [F], { in(F, l_XIAN_FINGER) }.
mf(move_finger(F)) --> [F], { in(F, l_MOVE_FINGER) }.

sf(special_finger({null})) --> [].
sf(special_finger(F)) --> [F], { in(F, l_SPECIAL_FINGER) }.

bf(both_finger(F)) --> [F], { in(F, l_BOTH_FINGER) }.
cf(complex_finger(F)) --> [F], { in(F, l_COMPLEX_FINGER) }.
modifier(modifier(M)) --> [M], { in(M, l_MODIFIER) }.
marker(marker(M)) --> [M], { in(M, l_MARKER) }.


%% number is an array of atoms
hnp(number({null})) --> [].
hnp(number(N)) --> hn(N).
hnp(number(N1,N2)) --> hn(N1), fn(N2).

hn(N) --> [N], { in(N, l_HUI) }.
fn(N) --> [N], { in(N, l_FEN) }.

xnp(number({null})) --> [].
xnp(number(N)) --> xn(N).
xnp(number(N1,N2)) --> xn(N1), xn(N2).
xn(N) --> [N], { in(N, l_XIAN) }.
