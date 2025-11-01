#
# Pittan Dictionary
# PittanDic.py 2025/11/01
#
import pyperclip
import pyxel
import pxt
import pim2

WIDTH = 344  # アプリ幅
INPUT_Y = 2
INPUT_MAX_CHARA = 32
INP_MEAN_XYWH = (36,INPUT_Y, INPUT_MAX_CHARA*8+16,28+12)  # 入力文字列の意味
INPUT_XYWH = (36,INP_MEAN_XYWH[1]+INP_MEAN_XYWH[3]-1+2, INPUT_MAX_CHARA*8+16,19)  # 入力枠
HEIGHT = INPUT_XYWH[1]+INPUT_XYWH[3]+27  # アプリ高さ
RET_BTN_XYWH = (WIDTH-32,INPUT_XYWH[1], 29,19)  #  RET（入力／確定）ボタン
BS_BTN_XYWH = (4,INPUT_XYWH[1]+23, 29,19)  # BS（削除）ボタン
TAB_BTN_XYWH = (WIDTH-32,INPUT_XYWH[1]+23, 29,19)  # TAB（候補）ボタン
CAND_LINE_BTN_XYWH = (INPUT_XYWH[0]+INPUT_XYWH[2]-22,INPUT_XYWH[1]+23, 22,19)  # 候補ライン変更ボタン
BG_COL = pyxel.COLOR_NAVY
FRAME_COL = pyxel.COLOR_CYAN
ALL_LETTER = 'アイウヴエオカガキギクグケゲコゴサザシジスズセゼソゾタダチヂツヅテデトドナニヌネノハバパヒビピフブプヘベペホボポマミムメモヤユヨラリルレロワ'
KATAKANA = list(range(0x30A1,0x30FA+1))+[0x30FC]  # カタカナ＋'ー'

hira2kata = lambda s: ''.join('ヴ' if c == 'ゔ' else chr(ord(c) + 0x60) if 'ぁ' <= c <= 'ゖ' else c for c in s)  # ひらがなカタカナ変換

class App:
    def in_cursor(self, xywh, dy=1):  # 範囲内1～／範囲外0
        for i in range(dy):
            if xywh[0]<=pyxel.mouse_x<xywh[0]+xywh[2] and xywh[1]+(xywh[3]*i)//dy<=pyxel.mouse_y<xywh[1]+(xywh[3]*(i+1))//dy:
                return i+1
        return 0

    def in_cursor_cand(self):  # 範囲内1～／範囲外0
        for i in range(len(self.pim2.cands_xw[self.pim2.cand_line])):
            if self.in_cursor((self.pim2.cands_xw[self.pim2.cand_line][i][0]+36,INPUT_XYWH[1]+23, self.pim2.cands_xw[self.pim2.cand_line][i][1],19)):
                return i+1
        return 0

    def __init__(self):
        pyxel.init(WIDTH,HEIGHT, title='Pittan Dictionary', display_scale=2, capture_scale=1, capture_sec=90)
        pyxel.mouse(True)
        self.pim2 = pim2.PyxelInputMethod()
        self.pim2.input_meaning = ''  # 入力文字列の意味
        self.pim2.initial_letter = ALL_LETTER  # すべての文字
        self.pim2.fixed_txt = ''  # 確定文字列
        self.pim2.entering_txt = ''  # 入力中文字列
        self.pim2.set_candidate(self.pim2.find_postfixes())  # 候補
        pyxel.run(self.update, self.draw) 

    def update(self):
        if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT):
            if self.in_cursor(BS_BTN_XYWH):  # BSボタン
                if self.pim2.entering_txt or self.pim2.fixed_txt:
                    self.pim2.backspace_btn()  # BSキー／ボタン
            elif self.in_cursor(RET_BTN_XYWH):  # RETボタン
                if self.pim2.entering_txt or self.pim2.cand_n!=None or self.pim2.input_meaning:
                    if self.pim2.return_btn()==3:  # RETキー／ボタン
                        pyperclip.copy(self.pim2.input_meaning_clip)  # クリップボード
                        self.pim2.fixed_txt = ''
                        self.pim2.set_candidate(self.pim2.find_postfixes())  # 候補
            elif self.in_cursor(TAB_BTN_XYWH):  # TABボタン
                self.pim2.right_key()
            elif len(self.pim2.cands)>1 and self.in_cursor(CAND_LINE_BTN_XYWH):  # 候補ボタン
                self.pim2.cand_line = (self.pim2.cand_line+1) % len(self.pim2.cands)
            elif self.pim2.cands!=[[]] and (pos := self.in_cursor_cand()):  # 次の文字候補
                self.pim2.fixed_txt += self.pim2.cands[self.pim2.cand_line][pos-1]
                self.pim2.set_input_meaning()  # 入力文字列の意味セット
                self.pim2.set_candidate(self.pim2.find_postfixes())  # 候補文字列セット
                self.pim2.entering_txt = ''  # 入力中文字列
                self.pim2.tab_cand_n = None
        if pyxel.btnr(pyxel.KEY_RETURN):  # RETキー
            if self.pim2.return_btn()==3:  # RETキー／ボタン
                pyperclip.copy(self.pim2.input_meaning_clip)  # クリップボード
                self.pim2.fixed_txt = ''
                self.pim2.set_candidate(self.pim2.find_postfixes())  # 候補
        elif pyxel.btnp(pyxel.KEY_BACKSPACE,10,2):  # BSキー
            self.pim2.backspace_btn()  # BSキー／ボタン
        elif pyxel.btnp(pyxel.KEY_TAB,10,2) or pyxel.btnp(pyxel.KEY_SPACE,10,2) or pyxel.btnp(pyxel.KEY_RIGHT,10,2):  # TABキー／SPCキー／右キー
            self.pim2.right_key()
        elif pyxel.btnp(pyxel.KEY_LEFT,10,2):  # 左キー
            self.pim2.left_key()
        elif pyxel.btnp(pyxel.KEY_DOWN,10,2):  # 下キー
            self.pim2.down_key()
        elif pyxel.btnp(pyxel.KEY_UP,10,2):  # 上キー
            self.pim2.up_key()
        elif pyxel.btnr(pyxel.MOUSE_BUTTON_RIGHT) or (pyxel.btn(pyxel.KEY_CTRL) and pyxel.btn(pyxel.KEY_V)):  # 右クリック／CTRL+V
            self.pim2.fixed_txt = ''
            self.pim2.entering_txt = ''
            s = hira2kata(pyperclip.paste())  # クリップボード
            for ch in s:
                if len(self.pim2.fixed_txt)<INPUT_MAX_CHARA:
                    if ord(ch) in KATAKANA:
                        self.pim2.fixed_txt += ch
                else:
                    break
            self.pim2.any_key('', changed=True)
        if sum(1 if ord(ch)<=0x7f else 2 for ch in self.pim2.fixed_txt+self.pim2.entering_txt)<INPUT_MAX_CHARA*2:
            self.pim2.any_key(pyxel.input_text)  # 文字入力(A～Z,a～z,-)

    def draw(self):
        pyxel.cls(BG_COL)
        if self.pim2.input_meaning:
            pxt.textbox(INP_MEAN_XYWH[0]+3, INP_MEAN_XYWH[1]+2, self.pim2.input_meaning, pyxel.COLOR_WHITE)  # 入力文字列の意味
        pyxel.rect(*INPUT_XYWH, pyxel.COLOR_BLACK)  # 入力（背景）
        pyxel.rectb(*INPUT_XYWH, FRAME_COL)  # 入力（枠）
        x = 5
        x += pxt.textline(INPUT_XYWH[0]+x,INPUT_XYWH[1]+4, self.pim2.fixed_txt, pyxel.COLOR_YELLOW if self.pim2.input_meaning else pyxel.COLOR_WHITE)  # 確定文字列
        x += pxt.textline(INPUT_XYWH[0]+x,INPUT_XYWH[1]+4, self.pim2.entering_txt, pyxel.COLOR_LIGHT_BLUE)  # 入力中文字列
        x += pxt.textline(INPUT_XYWH[0]+x,INPUT_XYWH[1]+4, '_' if pyxel.frame_count//20%2 else '', pyxel.COLOR_WHITE)  # 点滅入力カーソル
        if self.pim2.entering_txt or self.pim2.fixed_txt:
            pyxel.elli(*BS_BTN_XYWH, pyxel.COLOR_ORANGE if self.in_cursor(BS_BTN_XYWH) else pyxel.COLOR_NAVY)  # BS（削除）ボタン（背景）
            pyxel.ellib(*BS_BTN_XYWH, FRAME_COL)  # BS（削除）ボタン（枠）
            pxt.textline(BS_BTN_XYWH[0]+7,BS_BTN_XYWH[1]+4, '削除', pyxel.COLOR_WHITE if self.in_cursor(BS_BTN_XYWH) else pyxel.COLOR_GRAY)  # BS（削除）ボタン
        if self.pim2.entering_txt or not self.pim2.cand_n==None or self.pim2.input_meaning:
            pyxel.elli(*RET_BTN_XYWH, pyxel.COLOR_ORANGE if self.in_cursor(RET_BTN_XYWH) else pyxel.COLOR_PURPLE 
                    if self.pim2.input_meaning and not self.pim2.entering_txt else pyxel.COLOR_NAVY)  # RET（入力／確定）ボタン（背景）
            pyxel.ellib(*RET_BTN_XYWH, FRAME_COL)  # RET（入力／確定）ボタン（枠）
            pxt.textline(RET_BTN_XYWH[0]+7,RET_BTN_XYWH[1]+4, '入力' if self.pim2.entering_txt or not self.pim2.cand_n==None else '確定', 
                    pyxel.COLOR_WHITE if self.in_cursor(RET_BTN_XYWH) else pyxel.COLOR_GRAY)  # RET（入力／確定）ボタン
        if not self.pim2.cands==[[]]:
            pyxel.elli(*TAB_BTN_XYWH, pyxel.COLOR_ORANGE if self.in_cursor(TAB_BTN_XYWH) else pyxel.COLOR_NAVY)  # TAB（候補）ボタン（背景）
            pyxel.ellib(*TAB_BTN_XYWH, FRAME_COL)  # TAB（候補）ボタン（枠）
            pxt.textline(TAB_BTN_XYWH[0]+7,TAB_BTN_XYWH[1]+4, '候補', pyxel.COLOR_WHITE if self.in_cursor(TAB_BTN_XYWH) else pyxel.COLOR_GRAY)  # TAB（候補）ボタン
            for i,c in enumerate(self.pim2.cands[self.pim2.cand_line]):
                xywh = (self.pim2.cands_xw[self.pim2.cand_line][i][0]+36,INPUT_XYWH[1]+23, self.pim2.cands_xw[self.pim2.cand_line][i][1],19)
                pyxel.rect(*xywh, pyxel.COLOR_ORANGE if self.in_cursor(xywh) else pyxel.COLOR_GREEN if i==self.pim2.cand_n else pyxel.COLOR_NAVY)  # 候補文字列ボタン（背景）
                pyxel.rectb(*xywh, FRAME_COL)  # 候補文字列ボタン（枠）
                pxt.textline(xywh[0]+6,xywh[1]+4, c, pyxel.COLOR_WHITE)  # 候補文字列ボタン
            if len(self.pim2.cands)>1:
                pyxel.rect(*CAND_LINE_BTN_XYWH, pyxel.COLOR_ORANGE if self.in_cursor(CAND_LINE_BTN_XYWH) else pyxel.COLOR_NAVY)  # 候補ライン変更ボタン（背景）
                pyxel.rectb(*CAND_LINE_BTN_XYWH, FRAME_COL)  # 候補ライン変更ボタン（枠）
                pxt.textline(CAND_LINE_BTN_XYWH[0]+4,CAND_LINE_BTN_XYWH[1]+4, f'{self.pim2.cand_line+1}／{len(self.pim2.cands)}', 7)  # 候補ライン変更ボタン

App()
