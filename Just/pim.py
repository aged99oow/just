#
# Pyxel Input Method
# pim.py 2025/10/18
#
import pwdic

RK_DICT_1C = {  # 1文字一致⇒1文字変換
        '0':'０', '1':'１', '2':'２', '3':'３', '4':'４',
        '5':'５', '6':'６', '7':'７', '8':'８', '9':'９',
        ' ':'　', '_':'＿',
        'a':'ア', 'i':'イ', 'u':'ウ', 'e':'エ', 'o':'オ',
        '-':'ー',}
RK_DICT_2X = {  # 2文字一致⇒1文字変換
        'bb':'ッ', 'cc':'ッ', 'dd':'ッ', 'ff':'ッ', 'gg':'ッ',
        'hh':'ッ', 'jj':'ッ', 'kk':'ッ', 'll':'ッ', 'mm':'ッ',
        'pp':'ッ', 'qq':'ッ', 'rr':'ッ', 'ss':'ッ', 'tt':'ッ',
        'vv':'ッ', 'ww':'ッ', 'xx':'ッ', 'yy':'ッ', 'zz':'ッ',
        'nb':'ン', 'nc':'ン', 'nd':'ン', 'nf':'ン', 'ng':'ン',
        'nh':'ン', 'nj':'ン', 'nk':'ン', 'nl':'ン', 'nm':'ン',
        'np':'ン', 'nq':'ン', 'nr':'ン', 'ns':'ン', 'nt':'ン',
        'nv':'ン', 'nx':'ン', 'nz':'ン',
        'mb':'ン', 'mc':'ン', 'md':'ン', 'mf':'ン', 'mg':'ン',
        'mh':'ン', 'mj':'ン', 'mk':'ン', 'ml':'ン', 'mn':'ン',
        'mp':'ン', 'mq':'ン', 'mr':'ン', 'ms':'ン', 'mt':'ン',
        'mv':'ン', 'mw':'ン', 'mx':'ン', 'mz':'ン',}
RK_DICT_2C = {  # 2文字一致⇒2文字変換
        'ka':'カ'  , 'ki':'キ'  , 'ku':'ク'  , 'ke':'ケ'  , 'ko':'コ',
        'sa':'サ'  , 'si':'シ'  , 'su':'ス'  , 'se':'セ'  , 'so':'ソ',
        'ta':'タ'  , 'ti':'チ'  , 'tu':'ツ'  , 'te':'テ'  , 'to':'ト',
        'ca':'カ'  , 'ci':'シ'  , 'cu':'ク'  , 'ce':'セ'  , 'co':'コ',
        'qa':'クァ', 'qi':'クィ', 'qu':'ク'  , 'qe':'クェ',  'qo':'クォ',
        'na':'ナ'  , 'ni':'ニ'  , 'nu':'ヌ'  , 'ne':'ネ'  , 'no':'ノ',
        'ha':'ハ'  , 'hi':'ヒ'  , 'fu':'フ'  , 'he':'ヘ'  , 'ho':'ホ',
        'fa':'ファ', 'fi':'フィ', 'fu':'フ'  , 'fe':'フェ', 'fo':'フォ',
        'ma':'マ'  , 'mi':'ミ'  , 'mu':'ム'  , 'me':'メ'  , 'mo':'モ',
        'ya':'ヤ'  , 'yi':'イ'  , 'yu':'ユ'  , 'ye':'イェ', 'yo':'ヨ',
        'ra':'ラ'  , 'ri':'リ'  , 'ru':'ル'  , 're':'レ'  , 'ro':'ロ',
        'wa':'ワ'  , 'wi':'ウィ', 'wu':'ウ'  , 'we':'ウェ', 'wo':'ヲ',
        'ga':'ガ'  , 'gi':'ギ'  , 'gu':'グ'  , 'ge':'ゲ'  , 'go':'ゴ',
        'za':'ザ'  , 'ji':'ジ'  , 'zu':'ズ'  , 'ze':'ゼ'  , 'zo':'ゾ',
        'ja':'ジャ', 'ji':'ジ'  , 'ju':'ジュ', 'je':'ジェ', 'jo':'ジョ',
        'da':'ダ'  , 'di':'ヂ'  , 'du':'ヅ'  , 'de':'デ'  , 'do':'ド',
        'ba':'バ'  , 'bi':'ビ'  , 'bu':'ブ'  , 'be':'ベ'  , 'bo':'ボ',
        'va':'ヴァ', 'vi':'ヴィ', 'vu':'ヴ'  , 've':'ヴェ', 'vo':'ヴォ',
        'pa':'パ'  , 'pi':'ピ'  , 'pu':'プ'  , 'pe':'ペ'  , 'po':'ポ',
        'xa':'ァ'  , 'xi':'ィ'  , 'xu':'ゥ'  , 'xe':'ェ'  , 'xo':'ォ', 
        'la':'ァ'  , 'li':'ィ'  , 'lu':'ゥ'  , 'le':'ェ'  , 'lo':'ォ',
        'nn':'ン',}
RK_DICT_2M = {  # 2文字不一致⇒1文字無変換
        'ky':'', 'kw':'', 'sy':'', 'sh':'', 'sw':'',
        'ty':'', 'th':'', 'ts':'', 'ch':'', 'cy':'',
        'ny':'', 'nw':'', 'hy':'', 'fy':'', 'my':'',
        'ry':'', 'gy':'', 'zy':'', 'jy':'',
        'dh':'', 'dy':'', 'by':'', 'vy':'', 'py':'',
        'xy':'', 'ly':'', 'lt':'', 'xt':'',}
RK_DICT_3C = {  # 3文字一致⇒3文字変換
        'kya':'キャ', 'kyi':'キィ', 'kyu':'キュ', 'kye':'キェ', 'kyo':'キョ',
        'kwa':'クヮ', 'kwi':'クィ', 'kwu':'クゥ', 'kwe':'クェ', 'kwo':'クォ',
        'sya':'シャ', 'syi':'シ'  , 'syu':'シュ', 'sye':'シェ', 'syo':'ショ',
        'sha':'シャ', 'shi':'シ'  , 'shu':'シュ', 'she':'シェ', 'sho':'ショ',
        'swa':'スヮ', 'swi':'スィ', 'swu':'スゥ', 'swe':'スェ', 'swo':'スォ',
        'tya':'チャ', 'tyi':'チィ', 'tyu':'チュ', 'tye':'チェ', 'tyo':'チョ',
        'tha':'テャ', 'thi':'ティ', 'thu':'テュ', 'the':'テェ', 'tho':'テョ',
        'tsa':'ツァ', 'tsi':'ツィ', 'tsu':'ツ'  , 'tse':'ツェ', 'tso':'ツォ',
        'cha':'チャ', 'chi':'チ'  , 'chu':'チュ', 'che':'チェ', 'cho':'チョ',
        'cya':'チャ', 'cyi':'チィ', 'cyu':'チュ', 'cye':'チェ', 'cyo':'チョ',
        'nya':'ニャ', 'nyi':'ニィ', 'nyu':'ニュ', 'nye':'ニェ', 'nyo':'ニョ',
        'nwa':'ヌヮ', 'nwi':'ヌィ', 'nwu':'ヌゥ', 'nwe':'ヌェ', 'nwo':'ヌォ',
        'hya':'ヒァ', 'hyi':'ヒィ', 'hyu':'ヒュ', 'hye':'ヒェ', 'hyo':'ヒョ',
        'fya':'フャ', 'fyi':'フィ', 'fyu':'フュ', 'fye':'フェ', 'fyo':'フョ',
        'mya':'ミャ', 'myi':'ミィ', 'myu':'ミュ', 'mye':'ミェ', 'myo':'ミョ',
        'rya':'リャ', 'ryi':'リィ', 'ryu':'リュ', 'rye':'リェ', 'ryo':'リョ',
        'gya':'ギャ', 'gyi':'ギィ', 'gyu':'ギュ', 'gye':'ギェ', 'gyo':'ギョ',
        'zya':'ジャ', 'zyi':'ジィ', 'zyu':'ジュ', 'zye':'ジェ', 'zyo':'ジョ',
        'jya':'ジャ', 'jyi':'ジィ', 'jyu':'ジュ', 'jye':'ジェ', 'jyo':'ジョ',
        'dha':'デャ', 'dhi':'ディ', 'dhu':'デュ', 'dhe':'デェ', 'dho':'デョ',
        'dya':'ヂャ', 'dyi':'ヂィ', 'dyu':'ヂュ', 'dye':'ヂェ', 'dyo':'ヂョ',
        'bya':'ビャ', 'byi':'ビィ', 'byu':'ビュ', 'bye':'ビェ', 'byo':'ビョ',
        'vya':'ヴャ', 'vyi':'ヴィ', 'vyu':'ヴュ', 'vye':'ヴェ', 'vyo':'ヴョ',
        'pya':'ピャ', 'pyi':'ピィ', 'pyu':'ピュ', 'pye':'ピェ', 'pyo':'ピョ',
        'xya':'ャ'  , 'xyi':'ィ'  , 'xyu':'ュ'  , 'xye':'ェ'  , 'xyo':'ョ',
        'lya':'ャ'  , 'lyi':'ィ'  , 'lyu':'ュ'  , 'lye':'ェ'  , 'lyo':'ョ',
        'ltu':'ッ'  , 'xtu':'ッ',}
RK_DICT_3M = {  # 3文字不一致⇒1文字無変換
        'lts':'', 'xts':'',}
RK_DICT_4C = {  # 4文字一致⇒4文字変換
        'ltsu':'ッ', 'xtsu':'ッ',}
BLACK,NAVY,PURPLE,GREEN,BROWN,DARKBLUE,LIGHTBLUE,WHITE,RED,ORANGE,YELLOW,LIME,CYAN,GRAY,PINK,PEACH = \
        '*0','*1','*2','*3','*4','*5','*6','*7','*8','*9','*A','*B','*C','*D','*E','*F'

class InputMethod:
    def __init__(self):
        self.fixed_txt = ''  # 確定文字列
        self.entering_txt = ''  # 入力中文字列

    def roma_kana(self, dict, chk_n, conv_n):  # ローマ字かな変換
        if len(self.entering_txt)>=chk_n:
            if kana := dict.get(self.entering_txt[:chk_n]):
                self.fixed_txt += kana
                self.entering_txt = self.entering_txt[conv_n:]

    def kana_nomatch(self, dict, chk_n):  # 入力中文字列1文字削除
        if len(self.entering_txt)>=chk_n and dict.get(self.entering_txt[:chk_n])==None:
            self.entering_txt = self.entering_txt[1:]

    def lowercase_key(self, key):  # アルファベット入力
        old_fixed_txt = self.fixed_txt
        old_entering_txt = self.entering_txt
        self.entering_txt += key
        self.roma_kana(RK_DICT_4C,4,4)  # 4文字一致⇒4文字変換
        self.kana_nomatch({},4)  # 4文字以上⇒1文字無変換
        self.roma_kana(RK_DICT_3C,3,3)  # 3文字一致⇒3文字変換
        self.kana_nomatch(RK_DICT_3M,3)  # 3文字不一致⇒1文字無変換
        self.roma_kana(RK_DICT_2C,2,2)  # 2文字一致⇒2文字変換
        self.roma_kana(RK_DICT_2X,2,1)  # 2文字一致⇒1文字変換
        self.kana_nomatch(RK_DICT_2M,2)  # 2文字不一致⇒1文字無変換
        self.roma_kana(RK_DICT_1C,1,1)  # 1文字一致⇒1文字変換
        if old_fixed_txt!=self.fixed_txt:
            return 2
        elif old_entering_txt!=self.entering_txt:
            return 1
        return 0

    def backspace_key(self):  # BSキー
        if self.entering_txt:  # 入力中文字列削除
            self.entering_txt = self.entering_txt[:-1]
            return 1
        elif self.fixed_txt:  # 確定文字列削除
            self.fixed_txt = self.fixed_txt[:-1]
            return 2
        return 0

class PyxelInputMethod(InputMethod):
    def __init__(self):
        super().__init__()
        self.input_meaning = ''  # 入力文字列の意味
        self.inpmean_popup_txt = ''  # 入力文字列の意味ポップアップ
        self.cands = [[]]  # 候補（2次元）
        self.cands_xw = []  # 候補のＸと幅
        self.cand_line = 0  # 候補の段数
        self.cand_n = None  # 候補の現段数の位置
        self.initial_letter = ''  # 頭文字

    def set_input_meaning(self):  # 入力文字列の意味
        self.input_meaning = ''
        meanings = pwdic.KANA_DIC.get(self.fixed_txt)
        if meanings:
            note = pwdic.form_txtbox(pwdic.form_notation(self.fixed_txt,meanings[0]),68,1,'','…')
            mean = pwdic.form_txtbox(meanings[1].rstrip('※＃'),68,1,'','…')
            self.input_meaning = YELLOW+note+'\n'+ORANGE+mean

    def find_postfixes(self):  # 次に続く文字列検索
        if self.fixed_txt=='':
            return list(self.initial_letter)
        strs = []  # 続く文字列
        chars = []  # 続く１文字
        fixed_len = len(self.fixed_txt)
        for reading in pwdic.KANA_DIC.keys():
            if reading.startswith(self.fixed_txt) and self.fixed_txt!=reading:  # 前方一致＆完全一致でない
                strs.append(reading[fixed_len:])
                chars.append(reading[fixed_len:fixed_len+1])
        postfixes = []
        for i,ch in enumerate(chars):
            postfixes.append(strs[i] if chars.count(ch)==1 else ch)  # 候補が１つなら文字列／そうでなければ１文字
        postfixes = list(set(postfixes))
        return postfixes

    def set_candidate(self, cand_strs):  # 候補文字列
        self.cands = []
        self.cands_xw = []
        self.cand_line = 0
        self.cand_n = None
        chunk = []
        chunk_xw = []
        chunk_len = 0
        for i,s in enumerate(cand_strs):
            cand_len = len(s)
            if chunk_len+cand_len>28:
                self.cands.append(chunk)
                self.cands_xw.append(chunk_xw)
                chunk = [s]
                chunk_xw =[(0,len(s)*8+12),]
                chunk_len = cand_len+2
            else:
                chunk.append(s)
                chunk_xw.append((chunk_len*8,len(s)*8+12))
                chunk_len += cand_len+2
        self.cands.append(chunk)
        self.cands_xw.append(chunk_xw)

    def return_btn(self):  # RETキー／ボタン
        if self.cand_n!=None:  # 候補確定
            self.entering_txt = ''
            self.fixed_txt += self.cands[self.cand_line][self.cand_n]
            self.set_input_meaning()  # 入力文字列の意味
            self.set_candidate(self.find_postfixes())  # 候補
            return 1
        elif self.entering_txt:  # 入力中文字列（アルファベット）クリア
            self.entering_txt = ''
            return 2
        elif self.input_meaning:  # 入力文字列の意味あり
            self.input_meaning = ''
            self.entering_txt = ''
            self.inpmean_popup_txt = ''
            return 3
        return 0

    def backspace_btn(self):  # BSキー／ボタン
        if self.backspace_key()==2:  # fixed_txt削除
            self.set_input_meaning()  # 入力文字列の意味
            self.set_candidate(self.find_postfixes())  # 候補
            return True
        return False

    def right_key(self):
        if self.cands!=[[]]:  # 候補あり
            self.entering_txt = ''
            if self.cand_n==None:
                self.cand_n = 0
            else:
                self.cand_n += 1
                if self.cand_n>=len(self.cands[self.cand_line]):
                    self.cand_n = 0
                    self.cand_line += 1
                    if self.cand_line>=len(self.cands):
                        self.cand_line = 0

    def left_key(self):
        if self.cands!=[[]]:  # 候補あり
            self.entering_txt = ''
            if self.cand_n==None:
                self.cand_n = 0
            else:
                self.cand_n -= 1
                if self.cand_n<0:
                    self.cand_line -= 1
                    if self.cand_line<0:
                        self.cand_line = len(self.cands)-1
                    self.cand_n = len(self.cands[self.cand_line])-1

    def down_key(self):
        if self.cands!=[[]]:  # 候補あり
            self.entering_txt = ''
            if self.cand_n!=None:
                self.cand_line += 1
                if self.cand_line>=len(self.cands):
                    self.cand_line = 0
            self.cand_n = 0

    def up_key(self):
        if not self.cands==[[]]:  # 候補あり
            self.entering_txt = ''
            if not self.cand_n==None:
                self.cand_line -= 1
                if self.cand_line<0:
                    self.cand_line = len(self.cands)-1
            self.cand_n = 0

    def any_key(self, input_txt):
        changed = False
        for key in input_txt:  # 文字入力(A～Z,a～z,-)
            key = key.lower()
            if not ('a'<=key<='z' or key=='-'):
                continue
            self.cand_n = None  # 候補クリア
            if self.lowercase_key(key)==2:  # fixed_txt変更
                if self.fixed_txt[0] in self.initial_letter:
                    changed = True
                else:
                    self.fixed_txt = ''  # 確定文字列
        if changed:
            self.set_input_meaning()  # 入力文字列の意味
            self.set_candidate(self.find_postfixes())  # 候補
        return changed


